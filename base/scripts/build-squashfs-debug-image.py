#!/usr/bin/env python3
import argparse
import binascii
import hashlib
import json
import math
import shutil
import struct
from dataclasses import dataclass, field
from pathlib import Path


SECTOR_SIZE = 512
CLUSTER_SIZE = 4096
SECTORS_PER_CLUSTER = CLUSTER_SIZE // SECTOR_SIZE
RESERVED_SECTORS = 32
NUM_FATS = 2
FAT_EOC = 0x0FFFFFFF
FAT_MEDIA = 0x0FFFFFF8
IH_MAGIC = 0x27051956
IH_OS_LINUX = 5
IH_ARCH_ARM64 = 22
IH_TYPE_SCRIPT = 6
IH_COMP_NONE = 0


@dataclass
class FatNode:
    name: str
    is_dir: bool
    data: bytes | None = None
    source: Path | None = None
    children: dict[str, "FatNode"] = field(default_factory=dict)
    parent: "FatNode | None" = None
    start_cluster: int = 0
    clusters: list[int] = field(default_factory=list)
    size: int = 0


def align_up(value: int, alignment: int) -> int:
    return ((value + alignment - 1) // alignment) * alignment


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {label}: {path}")


def read_bytes(path: Path) -> bytes:
    with path.open("rb") as f:
        return f.read()


def add_file(root: FatNode, rel: str, *, source: Path | None = None, data: bytes | None = None) -> None:
    if source is None and data is None:
        raise ValueError(f"No source or data for {rel}")
    parts = [part for part in rel.replace("\\", "/").split("/") if part]
    if not parts:
        raise ValueError("Empty FAT path")
    node = root
    for part in parts[:-1]:
        child = node.children.get(part)
        if child is None:
            child = FatNode(part, True, parent=node)
            node.children[part] = child
        elif not child.is_dir:
            raise ValueError(f"Path component is already a file: {part}")
        node = child
    leaf = parts[-1]
    size = len(data) if data is not None else source.stat().st_size
    node.children[leaf] = FatNode(leaf, False, data=data, source=source, parent=node, size=size)


def dos_datetime() -> tuple[int, int]:
    date = ((2026 - 1980) << 9) | (7 << 5) | 13
    time = (1 << 11) | (17 << 5) | 0
    return date, time


def sanitize_short_part(text: str) -> str:
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$%'-_@~`!(){}^#&")
    out = []
    for ch in text.upper():
        out.append(ch if ch in allowed else "_")
    return "".join(out).strip(" .") or "FILE"


def split_name(name: str) -> tuple[str, str]:
    if "." in name and not name.startswith("."):
        base, ext = name.rsplit(".", 1)
        return base, ext
    return name, ""


def short_name_for(name: str, used: set[bytes]) -> bytes:
    base, ext = split_name(name)
    clean_base = sanitize_short_part(base)
    clean_ext = sanitize_short_part(ext)[:3]

    simple = (
        name.upper() == name
        and len(clean_base) <= 8
        and len(clean_ext) <= 3
        and clean_base == base.upper()
        and (not ext or clean_ext == ext.upper())
    )
    if simple:
        candidate = clean_base[:8].ljust(8) + clean_ext.ljust(3)
        raw = candidate.encode("ascii")
        if raw not in used:
            used.add(raw)
            return raw

    stem = clean_base[:6]
    for i in range(1, 100000):
        suffix = f"~{i}"
        alias_base = (stem[: 8 - len(suffix)] + suffix).ljust(8)
        alias = (alias_base + clean_ext.ljust(3)).encode("ascii")
        if alias not in used:
            used.add(alias)
            return alias
    raise RuntimeError(f"Unable to allocate FAT short name for {name}")


def lfn_checksum(short_name: bytes) -> int:
    total = 0
    for value in short_name:
        total = (((total & 1) << 7) + (total >> 1) + value) & 0xFF
    return total


def utf16_units(name: str) -> list[int]:
    data = name.encode("utf-16le")
    return [data[i] | (data[i + 1] << 8) for i in range(0, len(data), 2)]


def build_lfn_entries(name: str, checksum: int) -> list[bytes]:
    units = utf16_units(name) + [0x0000]
    while len(units) % 13:
        units.append(0xFFFF)
    chunks = [units[i : i + 13] for i in range(0, len(units), 13)]
    entries: list[bytes] = []
    for seq in range(len(chunks), 0, -1):
        chunk = chunks[seq - 1]
        entry = bytearray(32)
        entry[0] = seq | (0x40 if seq == len(chunks) else 0)
        entry[11] = 0x0F
        entry[12] = 0
        entry[13] = checksum
        entry[26:28] = b"\x00\x00"
        offsets = [1, 3, 5, 7, 9, 14, 16, 18, 20, 22, 24, 28, 30]
        for off, unit in zip(offsets, chunk):
            struct.pack_into("<H", entry, off, unit)
        entries.append(bytes(entry))
    return entries


def make_dir_entry(name_raw: bytes, attr: int, cluster: int, size: int) -> bytes:
    date, time = dos_datetime()
    entry = bytearray(32)
    entry[0:11] = name_raw
    entry[11] = attr
    struct.pack_into("<H", entry, 14, time)
    struct.pack_into("<H", entry, 16, date)
    struct.pack_into("<H", entry, 18, date)
    struct.pack_into("<H", entry, 20, (cluster >> 16) & 0xFFFF)
    struct.pack_into("<H", entry, 22, time)
    struct.pack_into("<H", entry, 24, date)
    struct.pack_into("<H", entry, 26, cluster & 0xFFFF)
    struct.pack_into("<I", entry, 28, size)
    return bytes(entry)


def directory_entry_count(node: FatNode) -> int:
    count = 0 if node.parent is None else 2
    used: set[bytes] = set()
    for child in sorted(node.children.values(), key=lambda item: (not item.is_dir, item.name.lower())):
        short_name = short_name_for(child.name, used)
        count += len(build_lfn_entries(child.name, lfn_checksum(short_name))) + 1
    return max(1, count)


def allocate_clusters(root: FatNode, max_clusters: int) -> int:
    next_cluster = 2

    def alloc(node: FatNode, count: int) -> None:
        nonlocal next_cluster
        if count <= 0:
            node.start_cluster = 0
            node.clusters = []
            return
        end = next_cluster + count
        if end - 1 > max_clusters + 1:
            raise RuntimeError("FAT32 boot partition is too small for selected files")
        node.clusters = list(range(next_cluster, end))
        node.start_cluster = node.clusters[0]
        next_cluster = end

    def walk_dirs(node: FatNode) -> None:
        entries = directory_entry_count(node)
        clusters = max(1, math.ceil(entries * 32 / CLUSTER_SIZE))
        node.size = clusters * CLUSTER_SIZE
        alloc(node, clusters)
        for child in sorted(node.children.values(), key=lambda item: item.name.lower()):
            if child.is_dir:
                walk_dirs(child)

    def walk_files(node: FatNode) -> None:
        for child in sorted(node.children.values(), key=lambda item: item.name.lower()):
            if child.is_dir:
                walk_files(child)
            else:
                clusters = math.ceil(child.size / CLUSTER_SIZE) if child.size else 0
                alloc(child, clusters)

    walk_dirs(root)
    walk_files(root)
    return next_cluster


def build_directory_data(node: FatNode) -> bytes:
    entries: list[bytes] = []
    if node.parent is not None:
        entries.append(make_dir_entry(b".          ", 0x10, node.start_cluster, 0))
        parent_cluster = node.parent.start_cluster if node.parent else node.start_cluster
        entries.append(make_dir_entry(b"..         ", 0x10, parent_cluster, 0))

    used: set[bytes] = set()
    for child in sorted(node.children.values(), key=lambda item: (not item.is_dir, item.name.lower())):
        short_name = short_name_for(child.name, used)
        checksum = lfn_checksum(short_name)
        entries.extend(build_lfn_entries(child.name, checksum))
        attr = 0x10 if child.is_dir else 0x20
        size = 0 if child.is_dir else child.size
        entries.append(make_dir_entry(short_name, attr, child.start_cluster, size))

    data = b"".join(entries)
    return data.ljust(len(node.clusters) * CLUSTER_SIZE, b"\x00")


def iter_nodes(root: FatNode):
    yield root
    for child in root.children.values():
        if child.is_dir:
            yield from iter_nodes(child)
        else:
            yield child


def calc_fat_layout(total_sectors: int) -> tuple[int, int, int]:
    fat_sectors = 1
    while True:
        data_sectors = total_sectors - RESERVED_SECTORS - (NUM_FATS * fat_sectors)
        if data_sectors <= 0:
            raise ValueError("Boot partition is too small")
        clusters = data_sectors // SECTORS_PER_CLUSTER
        needed = math.ceil((clusters + 2) * 4 / SECTOR_SIZE)
        if needed == fat_sectors:
            return fat_sectors, data_sectors, clusters
        fat_sectors = needed


def make_boot_sector(total_sectors: int, fat_sectors: int, hidden_sectors: int, volume_id: int) -> bytes:
    sector = bytearray(SECTOR_SIZE)
    sector[0:3] = b"\xEB\x58\x90"
    sector[3:11] = b"MSWIN4.1"
    struct.pack_into("<H", sector, 11, SECTOR_SIZE)
    sector[13] = SECTORS_PER_CLUSTER
    struct.pack_into("<H", sector, 14, RESERVED_SECTORS)
    sector[16] = NUM_FATS
    struct.pack_into("<H", sector, 17, 0)
    struct.pack_into("<H", sector, 19, 0)
    sector[21] = 0xF8
    struct.pack_into("<H", sector, 22, 0)
    struct.pack_into("<H", sector, 24, 63)
    struct.pack_into("<H", sector, 26, 255)
    struct.pack_into("<I", sector, 28, hidden_sectors)
    struct.pack_into("<I", sector, 32, total_sectors)
    struct.pack_into("<I", sector, 36, fat_sectors)
    struct.pack_into("<H", sector, 40, 0)
    struct.pack_into("<H", sector, 42, 0)
    struct.pack_into("<I", sector, 44, 2)
    struct.pack_into("<H", sector, 48, 1)
    struct.pack_into("<H", sector, 50, 6)
    sector[64] = 0x80
    sector[66] = 0x29
    struct.pack_into("<I", sector, 67, volume_id)
    sector[71:82] = b"UGOS_BOOT  "
    sector[82:90] = b"FAT32   "
    sector[510:512] = b"\x55\xAA"
    return bytes(sector)


def make_fsinfo(free_clusters: int, next_cluster: int) -> bytes:
    sector = bytearray(SECTOR_SIZE)
    struct.pack_into("<I", sector, 0, 0x41615252)
    struct.pack_into("<I", sector, 484, 0x61417272)
    struct.pack_into("<I", sector, 488, free_clusters)
    struct.pack_into("<I", sector, 492, next_cluster)
    struct.pack_into("<I", sector, 508, 0xAA550000)
    return bytes(sector)


def build_fat32_image(image: Path, root: FatNode, total_sectors: int, hidden_sectors: int, volume_id: int) -> dict:
    fat_sectors, data_sectors, cluster_count = calc_fat_layout(total_sectors)
    next_cluster = allocate_clusters(root, cluster_count)
    used_clusters = next_cluster - 2
    free_clusters = cluster_count - used_clusters

    fat = [0] * (cluster_count + 2)
    fat[0] = FAT_MEDIA
    fat[1] = FAT_EOC
    for node in iter_nodes(root):
        for idx, cluster in enumerate(node.clusters):
            fat[cluster] = node.clusters[idx + 1] if idx + 1 < len(node.clusters) else FAT_EOC

    image.parent.mkdir(parents=True, exist_ok=True)
    with image.open("wb") as f:
        f.truncate(total_sectors * SECTOR_SIZE)
        boot = make_boot_sector(total_sectors, fat_sectors, hidden_sectors, volume_id)
        fsinfo = make_fsinfo(free_clusters, next_cluster)
        f.seek(0)
        f.write(boot)
        f.seek(SECTOR_SIZE)
        f.write(fsinfo)
        f.seek(6 * SECTOR_SIZE)
        f.write(boot)
        f.seek(7 * SECTOR_SIZE)
        f.write(fsinfo)

        fat_bytes = bytearray(fat_sectors * SECTOR_SIZE)
        for cluster, value in enumerate(fat):
            if cluster * 4 + 4 <= len(fat_bytes):
                struct.pack_into("<I", fat_bytes, cluster * 4, value & 0x0FFFFFFF)
        fat_start = RESERVED_SECTORS * SECTOR_SIZE
        for fat_index in range(NUM_FATS):
            f.seek(fat_start + fat_index * fat_sectors * SECTOR_SIZE)
            f.write(fat_bytes)

        data_start = (RESERVED_SECTORS + NUM_FATS * fat_sectors) * SECTOR_SIZE

        def write_cluster(cluster: int, data: bytes) -> None:
            offset = data_start + (cluster - 2) * CLUSTER_SIZE
            f.seek(offset)
            f.write(data.ljust(CLUSTER_SIZE, b"\x00"))

        for node in iter_nodes(root):
            if node.is_dir:
                payload = build_directory_data(node)
            elif node.data is not None:
                payload = node.data
            else:
                payload = read_bytes(node.source)
            for idx, cluster in enumerate(node.clusters):
                start = idx * CLUSTER_SIZE
                write_cluster(cluster, payload[start : start + CLUSTER_SIZE])

    return {
        "filesystem": "fat32",
        "label": "UGOS_BOOT",
        "bytes": total_sectors * SECTOR_SIZE,
        "sectors": total_sectors,
        "fat_sectors": fat_sectors,
        "cluster_size": CLUSTER_SIZE,
        "cluster_count": cluster_count,
        "used_clusters": used_clusters,
        "free_clusters": free_clusters,
    }


def make_mbr(disk_signature: int, partitions: list[dict]) -> bytes:
    mbr = bytearray(SECTOR_SIZE)
    struct.pack_into("<I", mbr, 440, disk_signature)
    for index, part in enumerate(partitions[:4]):
        entry = bytearray(16)
        entry[0] = 0x00
        entry[1:4] = b"\xFE\xFF\xFF"
        entry[4] = part["type"]
        entry[5:8] = b"\xFE\xFF\xFF"
        struct.pack_into("<I", entry, 8, part["start_lba"])
        struct.pack_into("<I", entry, 12, part["sectors"])
        mbr[446 + index * 16 : 446 + (index + 1) * 16] = entry
    mbr[510:512] = b"\x55\xAA"
    return bytes(mbr)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_uboot_script_image(script: str, name: str = "UGOS-ZERO3") -> bytes:
    data = script.encode("ascii")
    timestamp = 0
    data_crc = binascii.crc32(data) & 0xFFFFFFFF
    name_bytes = name.encode("ascii")[:32].ljust(32, b"\x00")
    header_without_crc = struct.pack(
        ">7I4B32s",
        IH_MAGIC,
        0,
        timestamp,
        len(data),
        0,
        0,
        data_crc,
        IH_OS_LINUX,
        IH_ARCH_ARM64,
        IH_TYPE_SCRIPT,
        IH_COMP_NONE,
        name_bytes,
    )
    header_crc = binascii.crc32(header_without_crc) & 0xFFFFFFFF
    header = struct.pack(
        ">7I4B32s",
        IH_MAGIC,
        header_crc,
        timestamp,
        len(data),
        0,
        0,
        data_crc,
        IH_OS_LINUX,
        IH_ARCH_ARM64,
        IH_TYPE_SCRIPT,
        IH_COMP_NONE,
        name_bytes,
    )
    return header + data


def copy_into(src: Path, dst: Path, offset: int, chunk_size: int = 1024 * 1024) -> None:
    with src.open("rb") as inf, dst.open("r+b") as outf:
        outf.seek(offset)
        shutil.copyfileobj(inf, outf, chunk_size)


def verify_image(path: Path, p2_offset: int) -> dict:
    with path.open("rb") as f:
        mbr = f.read(SECTOR_SIZE)
        f.seek(p2_offset)
        squashfs_magic = f.read(4)
    return {
        "mbr_signature_ok": mbr[510:512] == b"\x55\xAA",
        "rootfs_squashfs_magic_ok": squashfs_magic == b"hsqs",
    }


def make_boot_tree(project_dir: Path, root_partuuid: str, cmdline_extra: str = "") -> tuple[FatNode, list[str]]:
    bootfs = project_dir / "staging" / "orangepi-zero3-bootfs"
    image = bootfs / "Image"
    dtb = bootfs / "dtb" / "allwinner" / "sun50i-h618-orangepi-zero3.dtb"
    require_file(image, "Orange Pi Zero 3 kernel Image")
    require_file(dtb, "Orange Pi Zero 3 DTB")

    extlinux = f"""TIMEOUT 30
DEFAULT UGOS-ZERO3

LABEL UGOS-ZERO3
  LINUX /Image
  FDT /dtb/allwinner/sun50i-h618-orangepi-zero3.dtb
  APPEND console=ttyS0,115200 root=PARTUUID={root_partuuid} rootfstype=squashfs rootwait ro earlycon loglevel=7 net.ifnames=0 biosdevname=0 panic=10 {cmdline_extra}
"""
    armbian_env = f"""verbosity=7
bootlogo=false
console=serial
fdtfile=sun50i-h618-orangepi-zero3.dtb
rootdev=PARTUUID={root_partuuid}
rootfstype=squashfs
extraargs=rootwait ro earlycon loglevel=7 net.ifnames=0 biosdevname=0 panic=10 {cmdline_extra}
"""
    boot_cmd = f"""setenv ugos_root PARTUUID={root_partuuid}
setenv ugos_dtb /dtb/allwinner/sun50i-h618-orangepi-zero3.dtb
setenv ugos_kernel /Image
setenv bootargs root=${{ugos_root}} rootwait rootfstype=squashfs ro console=ttyS0,115200 earlycon loglevel=7 net.ifnames=0 biosdevname=0 panic=10 {cmdline_extra}
echo Loading UGOS Zero3 fallback boot script
echo devtype=${{devtype}} devnum=${{devnum}} distro_bootpart=${{distro_bootpart}}
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{kernel_addr_r}} ${{ugos_kernel}}
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{fdt_addr_r}} ${{ugos_dtb}}
fdt addr ${{fdt_addr_r}}
fdt resize 65536
booti ${{kernel_addr_r}} - ${{fdt_addr_r}}
"""
    boot_scr = make_uboot_script_image(boot_cmd)
    readme = f"""UGOS Pro ARM Orange Pi Zero 3 squashfs debug image

This is a first-boot diagnostic image.
Boot flow: U-Boot/SPL -> FAT32 /extlinux/extlinux.conf or /boot.scr -> Image + Orange Pi Zero 3 DTB -> UGOS rootfs-base.squashfs.
Rootfs PARTUUID: {root_partuuid}
"""

    root = FatNode("", True)
    add_file(root, "Image", source=image)
    add_file(root, "dtb/allwinner/sun50i-h618-orangepi-zero3.dtb", source=dtb)
    add_file(root, "extlinux/extlinux.conf", data=extlinux.encode("ascii"))
    add_file(root, "boot/extlinux/extlinux.conf", data=extlinux.encode("ascii"))
    add_file(root, "boot.cmd", data=boot_cmd.encode("ascii"))
    add_file(root, "boot.scr", data=boot_scr)
    add_file(root, "boot.scr.uimg", data=boot_scr)
    add_file(root, "armbianEnv.txt", data=armbian_env.encode("ascii"))
    add_file(root, "README-UGOS-ZERO3.txt", data=readme.encode("ascii"))
    files = [
        "/Image",
        "/dtb/allwinner/sun50i-h618-orangepi-zero3.dtb",
        "/extlinux/extlinux.conf",
        "/boot/extlinux/extlinux.conf",
        "/boot.cmd",
        "/boot.scr",
        "/boot.scr.uimg",
        "/armbianEnv.txt",
        "/README-UGOS-ZERO3.txt",
    ]
    return root, files


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a first-boot UGOS ARM Orange Pi Zero 3 debug SD image.")
    parser.add_argument("--project-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--out-image", default=None)
    parser.add_argument("--boot-mib", type=int, default=512)
    parser.add_argument("--disk-signature", default="0x55473033")
    parser.add_argument("--cmdline-extra", default="")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    out_image = Path(args.out_image).resolve() if args.out_image else project_dir / "out" / "ugos-opi-zero3-squashfs-debug.img"
    work_dir = project_dir / "work" / "squashfs-debug-image"
    boot_part_image = work_dir / "boot-fat32.img"
    manifest_path = out_image.with_suffix(out_image.suffix + ".manifest.json")
    sha_path = out_image.with_suffix(out_image.suffix + ".sha256")

    disk_signature = int(args.disk_signature, 16 if str(args.disk_signature).lower().startswith("0x") else 10)
    if not 0 <= disk_signature <= 0xFFFFFFFF:
        raise ValueError("disk signature must fit in 32 bits")
    root_partuuid = f"{disk_signature:08x}-02"

    bootloader = project_dir / "staging" / "orangepi-zero3-bootloader" / "u-boot-sunxi-with-spl.bin"
    rootfs = project_dir / "payload" / "rootfs-base.squashfs"
    require_file(bootloader, "Orange Pi Zero 3 U-Boot/SPL")
    require_file(rootfs, "UGOS rootfs-base.squashfs")

    boot_tree, boot_files = make_boot_tree(project_dir, root_partuuid, args.cmdline_extra.strip())
    boot_sectors = args.boot_mib * 1024 * 1024 // SECTOR_SIZE
    p1_start_lba = 16 * 1024 * 1024 // SECTOR_SIZE
    p1_sectors = boot_sectors
    p2_start_lba = align_up(p1_start_lba + p1_sectors, 2048)
    p2_sectors = align_up(rootfs.stat().st_size, 4 * 1024 * 1024) // SECTOR_SIZE
    end_lba = p2_start_lba + p2_sectors
    image_size = end_lba * SECTOR_SIZE

    boot_info = build_fat32_image(boot_part_image, boot_tree, p1_sectors, p1_start_lba, disk_signature)

    partitions = [
        {
            "number": 1,
            "type": 0x0C,
            "type_name": "W95 FAT32 LBA",
            "label": "UGOS_BOOT",
            "start_lba": p1_start_lba,
            "sectors": p1_sectors,
            "bytes": p1_sectors * SECTOR_SIZE,
            "partuuid": f"{disk_signature:08x}-01",
        },
        {
            "number": 2,
            "type": 0x83,
            "type_name": "Linux squashfs root",
            "label": "UGOS_ROOT_SQUASHFS",
            "start_lba": p2_start_lba,
            "sectors": p2_sectors,
            "bytes": p2_sectors * SECTOR_SIZE,
            "source_bytes": rootfs.stat().st_size,
            "partuuid": root_partuuid,
        },
    ]

    out_image.parent.mkdir(parents=True, exist_ok=True)
    with out_image.open("wb") as f:
        f.truncate(image_size)
        f.seek(0)
        f.write(make_mbr(disk_signature, partitions))

    copy_into(bootloader, out_image, 8 * 1024)
    copy_into(boot_part_image, out_image, p1_start_lba * SECTOR_SIZE)
    copy_into(rootfs, out_image, p2_start_lba * SECTOR_SIZE)

    verification = verify_image(out_image, p2_start_lba * SECTOR_SIZE)
    digest = sha256_file(out_image)
    sha_path.write_text(f"{digest}  {out_image.name}\n", encoding="ascii")

    manifest = {
        "image": str(out_image),
        "image_bytes": image_size,
        "sha256": digest,
        "disk_signature": f"0x{disk_signature:08x}",
        "root_partuuid": root_partuuid,
        "bootloader": str(bootloader),
        "bootloader_write_offset": 8 * 1024,
        "rootfs": str(rootfs),
        "cmdline_extra": args.cmdline_extra.strip(),
        "partitions": partitions,
        "boot_partition": boot_info,
        "boot_files": boot_files,
        "verification": verification,
        "notes": [
            "First-boot diagnostic image only.",
            "Root partition is the original UGOS rootfs-base.squashfs, mounted read-only.",
            "No UGOS rootfs patch tar is applied in this Windows-only squashfs image.",
            "Use serial console on ttyS0 at 115200 baud for first boot logs.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote image: {out_image}")
    print(f"Wrote manifest: {manifest_path}")
    print(f"Wrote sha256: {sha_path}")
    print(f"Root PARTUUID: {root_partuuid}")
    print(f"Image size: {image_size} bytes")
    print(f"Verification: {verification}")


if __name__ == "__main__":
    main()
