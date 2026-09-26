"""Server-side catalog generator v2: per-file subprocess isolation (OOM-safe).

Parent scans /www/packages/**.upk, spawns itself per file (--one) to extract
metadata, assembles the signed repo.json (community-store Ed25519 format).
"""
import gzip
import hashlib
import io
import json
import base64
import subprocess
import sys
import tarfile
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

PKG_ROOT = Path("/www/packages")
OUT = Path("/www/store/repo.json")
KEY = Path("/etc/ugos-store/signing-key.pem")


def canonical(value):
    if value is None or not isinstance(value, (dict, list)):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ",".join(canonical(v) for v in value) + "]"
    keys = sorted(value.keys())
    return "{" + ",".join(json.dumps(k) + ":" + canonical(value[k]) for k in keys) + "}"


def parse_field_blob(data: bytes, field: bytes) -> bytes:
    marker = field + b":"
    start = data.find(marker)
    length_start = start + len(marker)
    length_end = data.find(b":", length_start)
    length = int(data[length_start:length_end])
    return data[length_end + 1 : length_end + 1 + length]


def one(path: str, arch: str):
    """Extract metadata for a single UPK. Runs in its own process (memory freed on exit)."""
    p = Path(path)
    h = hashlib.sha256()
    size = 0
    buf = bytearray()
    with p.open("rb") as f:
        while True:
            chunk = f.read(8 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
            if len(buf) < 400 * 1024 * 1024:  # config.json lives near the head of the blob
                buf.extend(chunk)
    cfg_bytes = bytes(buf)
    del buf
    payload_gz = parse_field_blob(cfg_bytes, b"ugb")
    del cfg_bytes
    payload_tar = gzip.GzipFile(fileobj=io.BytesIO(payload_gz)).read()
    del payload_gz
    with tarfile.open(fileobj=io.BytesIO(payload_tar), mode="r:") as tar:
        ugb = [m for m in tar.getmembers() if m.name.endswith(".ugb")]
        inner = tar.extractfile(ugb[0]).read()
    del payload_tar
    cfg = None
    with tarfile.open(fileobj=io.BytesIO(inner), mode="r:*") as tar:
        for member in tar.getmembers():
            if member.name.split("/")[-1] == "config.json":
                cfg = json.loads(tar.extractfile(member).read().decode("utf-8"))
                break
    del inner
    if cfg is None:
        raise ValueError("config.json not found")
    ver = cfg.get("version")
    version = ver.get("version", "") if isinstance(ver, dict) else str(ver)
    meta = {
        "id": cfg.get("appId", ""),
        "name": p.stem.split("_v")[0] if "_v" in p.stem else cfg.get("appId", ""),
        "version": version,
        "arch": arch,
        "description": f"UGOS Pro app {cfg.get('appId','')}",
        "minFirmware": "1.17.0",
        "url": "packages/" + urllib.parse.quote(arch + "/" + p.name),
        "size": size,
        "sha256": h.hexdigest(),
    }
    print(json.dumps(meta, ensure_ascii=False))


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--one":
        one(sys.argv[2], sys.argv[3])
        return
    key = serialization.load_pem_private_key(KEY.read_bytes(), password=None)
    assert isinstance(key, Ed25519PrivateKey)
    pub_der = key.public_key().public_bytes(
        serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    key_id = hashlib.sha256(pub_der).hexdigest()[:16]

    files = []
    for arch_dir in sorted(PKG_ROOT.iterdir()):
        if arch_dir.is_dir():
            for upk in sorted(arch_dir.glob("*.upk")):
                files.append((upk, arch_dir.name))
    print(f"scanning {len(files)} UPKs ...", flush=True)

    packages = []
    skipped = []
    for i, (upk, arch) in enumerate(files):
        proc = subprocess.run(
            [sys.executable, "-u", __file__, "--one", str(upk), arch],
            capture_output=True, text=True, timeout=900,
        )
        if proc.returncode != 0:
            skipped.append((str(upk), (proc.stderr or "unknown").strip()[-160:]))
            print(f"[{i+1}/{len(files)}] SKIP {upk.name}: {(proc.stderr or 'unknown').strip()[-120:]}", flush=True)
            continue
        packages.append(json.loads(proc.stdout.strip().splitlines()[-1]))
        print(f"[{i+1}/{len(files)}] {upk.name} ok", flush=True)

    signed = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "packages": packages,
    }
    signature = key.sign(canonical(signed).encode("utf-8"))
    repo = {
        "signed": signed,
        "signature": {
            "algorithm": "Ed25519",
            "keyId": key_id,
            "value": base64.b64encode(signature).decode("ascii"),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(repo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"catalog written: {OUT} with {len(packages)} packages, {len(skipped)} skipped", flush=True)


if __name__ == "__main__":
    main()
