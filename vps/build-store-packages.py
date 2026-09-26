"""Extract all UPKs from ugreen.bz2 payload and build community-store package metadata."""
import gzip
import io
import json
import shutil
import tarfile
from pathlib import Path

PAYLOAD = Path(r"H:\ugos\payload\ugreen.bz2")
STORE = Path(r"H:\ugos\x86\ugos-community-store")
PKG_DIR = STORE / "packages"
META_DIR = STORE / "packages"


def parse_field_blob(data: bytes, field: bytes) -> bytes:
    marker = field + b":"
    start = data.find(marker)
    if start == -1:
        raise ValueError(f"missing {field.decode()} field")
    length_start = start + len(marker)
    length_end = data.find(b":", length_start)
    length = int(data[length_start:length_end])
    return data[length_end + 1 : length_end + 1 + length]


def upk_config(upk_bytes: bytes) -> dict:
    payload_gz = parse_field_blob(upk_bytes, b"ugb")
    with gzip.GzipFile(fileobj=io.BytesIO(payload_gz)) as gz:
        payload_tar = gz.read()
    with tarfile.open(fileobj=io.BytesIO(payload_tar), mode="r:") as tar:
        ugb_names = [m for m in tar.getmembers() if m.name.endswith(".ugb")]
        if not ugb_names:
            raise ValueError("no .ugb in payload tar")
        inner = tar.extractfile(ugb_names[0]).read()
    with tarfile.open(fileobj=io.BytesIO(inner), mode="r:*") as tar:
        for member in tar.getmembers():
            if member.name.split("/")[-1] == "config.json":
                return json.loads(tar.extractfile(member).read().decode("utf-8"))
    raise ValueError("config.json not found in UPK")


def main():
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    t = tarfile.open(PAYLOAD, "r:*")
    members = {Path(m.name).name: m for m in t.getmembers() if m.isfile()}
    upk_names = sorted(n for n in members if n.endswith(".upk"))
    print(f"found {len(upk_names)} UPKs in payload")
    results = []
    for name in upk_names:
        raw = t.extractfile(members[name]).read()
        try:
            cfg = upk_config(raw)
        except Exception as exc:
            print(f"  SKIP {name}: {exc}")
            continue
        out_name = name  # e.g. 08_arm64_com.ugreen.filemgr.upk
        (PKG_DIR / out_name).write_bytes(raw)
        ver = cfg.get("version")
        version = ver.get("version", "") if isinstance(ver, dict) else str(ver)
        meta = {
            "id": cfg.get("appId", ""),
            "name": cfg.get("appId", "").replace("com.ugreen.", ""),
            "version": version,
            "arch": "arm64" if "_arm64_" in name else "unknown",
            "description": f"UGREEN UGOS Pro app ({meta_app(cfg)})" if False else f"UGOS Pro app {cfg.get('appId','')}",
            "file": out_name,
        }
        meta_path = META_DIR / (out_name + ".package.json")
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        results.append((out_name, meta["id"], meta["name"], meta["version"], len(raw)))
        print(f"  {out_name}: id={meta['id']} name={meta['name']} v{meta['version']} {len(raw)//1024//1024}MB")
    print(f"prepared {len(results)} packages with metadata")


if __name__ == "__main__":
    main()
