"""UGOS official firmware monitor/sync.

Scans UGREEN's download center for all NAS products, registers firmware by
architecture (parsed from official filenames), downloads new releases, and
keeps a registry.  Designed for a systemd timer on the store VPS.
"""
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://www.ugnas.com"
API = "https://api-zh.ugnas.com"
STATE = Path("/srv/ugos/monitor-state.json")
OFFICIAL = Path("/www/official")
UA = {"User-Agent": "Mozilla/5.0"}
# UGREEN rate-limits aggressive scanning; be polite (one run/day, spaced requests)
DELAY_PAGE = 3.0
DELAY_RESOLVE = 1.5


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", errors="replace")


def product_ids():
    d = fetch(f"{BASE}/support/download-list/product_type=nas")
    ids = sorted({int(x) for x in re.findall(r"product_type=nas&id=(\d+)", d)})
    return ids


def resolve_temp(url):
    d = fetch(url)
    j = json.loads(d)
    return j["data"]["linkData"]["tempUrl"]


def product_firmwares(pid):
    """Return [{version, date, size, md5, temp_url, real_url, filename, arch, soc}]"""
    time.sleep(DELAY_PAGE)
    d = fetch(f"{BASE}/support/download-list/product_type=nas&id={pid}&type=2")
    hrefs = re.findall(r'download_href="([^"]+)"', d)
    out = []
    seen = set()
    for h in hrefs:
        m = re.search(r"appType=firmware&id=(\d+)", h)
        if not m:
            continue
        fid = m.group(1)
        if fid in seen:
            continue
        seen.add(fid)
        i = d.find(h)
        block = d[max(0, i - 1500) : i]
        ver = (re.findall(r"版本：([^\n<]+)", block) or [""])[-1].strip()
        date = (re.findall(r"发布日期：([^\n<]+)", block) or [""])[-1].strip()
        size = (re.findall(r"文件大小：([^\n<]+)", block) or [""])[-1].strip()
        md5 = (re.findall(r'ly-text-copy="([0-9a-f]{32})"', block) or [""])[-1]
        real, rerr = "", ""
        for attempt in range(3):
            try:
                time.sleep(DELAY_RESOLVE)
                real = resolve_temp(h)
                rerr = ""
                break
            except Exception as exc:
                rerr = str(exc)
                time.sleep(5 * (attempt + 1))
        if real:
            fname = real.split("?")[0].rsplit("/", 1)[-1]
            arch = "arm64" if "_arm64_" in fname else ("amd64" if "_amd64_" in fname else "unknown")
            soc_m = re.search(r"-(intel|rk35\d{2}[a-z]?|rk35\d{2}|amlogic|n5105|n100|n97)(?:_|-|\.)", fname)
            out.append(
                {
                    "fw_id": fid,
                    "version": ver,
                    "date": date,
                    "size": size,
                    "md5": md5,
                    "temp_url": h,
                    "real_url": real,
                    "filename": fname,
                    "arch": arch,
                    "soc": soc_m.group(1) if soc_m else "",
                }
            )
        else:
            out.append({"fw_id": fid, "version": ver, "date": date, "size": size, "md5": md5, "error": rerr})
    return out


def download(url, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp, dest.open("wb") as f:
        while True:
            chunk = resp.read(4 * 1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    return dest


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    reg = state.setdefault("firmwares", {})
    ids = product_ids()
    print(f"{datetime.now(timezone.utc).isoformat()} scanning {len(ids)} products", flush=True)
    for pid in ids:
        try:
            fws = product_firmwares(pid)
        except Exception as exc:
            print(f"  product {pid}: scan error {exc}", flush=True)
            continue
        for fw in fws:
            if "error" in fw:
                continue
            key = f"{pid}:{fw['fw_id']}"
            new = key not in reg
            reg[key] = {**fw, "product_id": pid, "seen_at": datetime.now(timezone.utc).isoformat()}
            if new:
                print(f"  NEW product={pid} fw_id={fw['fw_id']} v{fw['version']} arch={fw['arch']} soc={fw['soc']} {fw['filename']}", flush=True)
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1))
        # keep only the newest firmware file per (product, arch) on disk
    latest = {}
    for key, fw in reg.items():
        if "filename" not in fw:
            continue
        slot = f"{fw['product_id']}:{fw['arch']}"
        cur = latest.get(slot)
        if cur is None or fw["version"] > cur["version"]:
            latest[slot] = fw
    for slot, fw in sorted(latest.items()):
        dest = OFFICIAL / f"product-{fw['product_id']}" / fw["filename"]
        if dest.exists() and dest.stat().st_size > 100 * 1024 * 1024:
            continue
        try:
            print(f"  downloading {fw['filename']} -> {dest}", flush=True)
            download(fw["real_url"], dest)
            print(f"  downloaded {dest.stat().st_size:,} bytes", flush=True)
        except Exception as exc:
            print(f"  download failed: {exc}", flush=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1))
    print("state saved", flush=True)


if __name__ == "__main__":
    main()
