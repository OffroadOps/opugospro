import struct
import sys

img = sys.argv[1] if len(sys.argv) > 1 else "radxa-cubie-a5e_bullseye_cli_r7.output_512.img"
TYPES = {
    0x0FC63DAF8482477E8E42D70992894BFD: "Linux fs",
    0xC12A7328F81F2D69BA88D0095B9AB9FB: "EFI System",
    0x0657FD6DA4AB43C484E5093C4450D9EB: "swap",
    0x2168614864496E6B74496E64696664494E: "BIOS boot",
    0xE6D6D379F50744C2A23C238F2A3DF928: "Linux LVM",
    0x933AB7E5EB7F4BDBB2DCF353EED0BF9A: "Android meta",
    0x19A710A2B3CA4D99AC54337D71A1D576: "Android boot",
    0x4989D98C4E124C88B38CB01EE5C6AA39: "Allwinner data",
}
f = open(img, "rb")
mbr = f.read(512)
print("MBR boot signature:", mbr[510:512].hex())
print("MBR p1 entry:", mbr[446:462].hex())
print("MBR p2 entry:", mbr[462:478].hex())
f.seek(512)
hdr = f.read(512)
print("LBA1 signature:", hdr[:8])
if hdr[:8] != b"EFI PART":
    sys.exit("not GPT")
num = struct.unpack_from("<I", hdr, 80)[0]
esz = struct.unpack_from("<I", hdr, 84)[0]
estart = struct.unpack_from("<Q", hdr, 72)[0]
print(f"GPT entries={num} entry_size={esz} entry_start_lba={estart}")
f.seek(estart * 512)
for i in range(num):
    e = f.read(esz)
    t = int.from_bytes(e[0:16], "little")
    first, last = struct.unpack_from("<QQ", e, 32)
    name = e[56:128].decode("utf-16-le").rstrip("\x00")
    if t == 0:
        continue
    tn = TYPES.get(t, hex(t))
    print(
        f"p{i+1}: type={tn:14s} start={first:>9} ({first*512/1048576:8.1f} MiB) "
        f"size={(last-first+1)*512/1048576:9.1f} MiB  name={name!r}"
    )
# first 4 KiB hexdump of offset 8KiB to identify bootloader
f.seek(8192)
head = f.read(64)
print("bytes@8KiB:", head[:32].hex())
f.seek(0)
head = f.read(64)
print("bytes@0   :", head[:32].hex())
