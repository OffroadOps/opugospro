import sys

img = "radxa-cubie-a5e_bullseye_cli_r7.output_512.img"
CHUNK = 65536
f = open(img, "rb")
runs = []
cur = None
pos = 0
end = 40 * 1024 * 1024
while pos < end:
    f.seek(pos)
    data = f.read(CHUNK)
    if not data:
        break
    nz = any(b != 0 for b in data)
    if nz and cur is None:
        cur = pos
    elif not nz and cur is not None:
        runs.append((cur, pos))
        cur = None
    pos += len(data)
if cur is not None:
    runs.append((cur, end))
for start, stop in runs:
    f.seek(start)
    head = f.read(48)
    print(f"non-zero: {start:>10} - {stop:>10}  ({(stop-start)/1048576:8.2f} MiB)  head={head[:32].hex()}  ascii={head[:24]!r}")

# check inside p1 region 16-32MiB for eGON / U-Boot strings
import re
f.seek(0)
data = f.read(40 * 1024 * 1024)
for sig in [b"eGON", b"u-boot", b"U-Boot", b"FIT", b"OHWARE", b"sun55i", b"BOOT0", b"boot0"]:
    idxs = [m.start() for m in re.finditer(re.escape(sig), data)][:6]
    if idxs:
        print(f"signature {sig!r} at: {idxs}")
