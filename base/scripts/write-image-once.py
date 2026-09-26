#!/usr/bin/env python3
"""One-shot physical-drive writer: open once, write image, fsync, readback-verify.

Replaces the zero-then-writer two-process dance whose Update-Disk rescan in
between could invalidate the device handle (Errno 9 / ERROR_INVALID_HANDLE).
The image itself overwrites sector 0, so stale partition tables on the first
sectors are replaced by the write; no separate zeroing pass is needed.
"""
import argparse
import hashlib
import json
import os
import time
from pathlib import Path

CHUNK = 1 * 1024 * 1024  # 8MiB chunks started failing with ERROR_INVALID_HANDLE on the
                         # degraded card reader; 1MiB passes reliably (zeroer proved it)
STATUS_STEP = 256 * 1024 * 1024


def update_status(path: Path, phase: str, completed: int, total: int, message: str = "") -> None:
    payload = {
        "phase": phase,
        "completed_bytes": completed,
        "total_bytes": total,
        "percent": round(completed * 100 / total, 2) if total else 0,
        "message": message,
        "updated_unix": time.time(),
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_all(handle, data: bytes) -> None:
    view = memoryview(data)
    while view:
        written = handle.write(view)
        if not written:
            raise OSError("physical-drive write returned zero bytes")
        view = view[written:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--device", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--raw-bytes", type=int, required=True)
    parser.add_argument("--status", type=Path, required=True)
    args = parser.parse_args()
    args.status.parent.mkdir(parents=True, exist_ok=True)

    if args.image.stat().st_size != args.raw_bytes:
        raise ValueError(f"raw image size mismatch: {args.image.stat().st_size}")
    src_digest = hashlib.sha256()
    with args.image.open("rb") as f:
        for chunk in iter(lambda: f.read(16 * 1024 * 1024), b""):
            src_digest.update(chunk)
    if src_digest.hexdigest().lower() != args.expected_sha256.lower():
        raise ValueError(f"raw image SHA256 mismatch: {src_digest.hexdigest()}")
    update_status(args.status, "write", 0, args.raw_bytes, "source verified; writing in one open handle")

    with args.image.open("rb") as source, open(args.device, "r+b", buffering=0) as target:
        target.seek(0)
        completed = 0
        next_status = STATUS_STEP
        while chunk := source.read(CHUNK):
            write_all(target, chunk)
            completed += len(chunk)
            if completed >= next_status:
                update_status(args.status, "write", completed, args.raw_bytes)
                next_status += STATUS_STEP
        target.flush()
        os.fsync(target.fileno())
    if completed != args.raw_bytes:
        raise ValueError(f"written byte count mismatch: {completed}")

    read_digest = hashlib.sha256()
    completed = 0
    next_status = STATUS_STEP
    update_status(args.status, "readback", 0, args.raw_bytes, "verifying complete write")
    with open(args.device, "rb", buffering=0) as target:
        while completed < args.raw_bytes:
            chunk = target.read(min(CHUNK, args.raw_bytes - completed))
            if not chunk:
                raise OSError(f"short read at byte {completed}")
            read_digest.update(chunk)
            completed += len(chunk)
            if completed >= next_status:
                update_status(args.status, "readback", completed, args.raw_bytes)
                next_status += STATUS_STEP
    if read_digest.hexdigest().lower() != args.expected_sha256.lower():
        raise ValueError(f"readback SHA256 mismatch: {read_digest.hexdigest()}")
    update_status(args.status, "complete", completed, args.raw_bytes, "full readback SHA256 matched")


if __name__ == "__main__":
    main()
