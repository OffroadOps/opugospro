import os
import io
import shutil
import struct
import subprocess
import sys
import tarfile
import time
import urllib.request
import uuid
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FW = ROOT / "release_20260825-firmware_image-1.19.1.126-intel_release_amd64_6.18_nasync.img"
ANALYSIS = ROOT / "_ugreen_analysis"
PAYLOAD = ROOT / "_ugreen_payload"
OUT = ROOT / "_out"

QEMU = ROOT / "_tools" / "qemu" / "extract" / "qemu-system-x86_64.exe"
QEMU_IMG = ROOT / "_tools" / "qemu" / "extract" / "qemu-img.exe"
SEVENZ = ROOT / "_tools" / "7zip" / "full" / "7z.exe"
GRUB_PC_URL = "https://deb.debian.org/debian/pool/main/g/grub2/grub-pc-bin_2.06-13+deb12u2_amd64.deb"
GRUB_PC_DEB = ROOT / "_tools" / "grub" / "grub-pc-bin_2.06-13+deb12u2_amd64.deb"
GRUB_PC_WORK = ROOT / "_tools" / "grub" / "grub-pc-bin"

IMAGE = OUT / "ugospro-1.19.1.126-amd64-universal-bios-uefi-gpt-dd.img"
SOURCE_ISO = OUT / "ugos_payload.iso"
BUILDER_CPIO = ANALYSIS / "builder-initrd.cpio"
BUILDER_INITRD = ANALYSIS / "builder-initrd.img"
BUILDER_KERNEL = ANALYSIS / "vmlinuz"
IMAGE_SIZE_GIB = 16
UGREEN_PARTITION_MIB = 8192
BIOS_BOOT_PARTITION_MIB = 2


def run(cmd, *, cwd=ROOT, check=True):
    print("+", " ".join(map(str, cmd)), flush=True)
    return subprocess.run(cmd, cwd=cwd, check=check)


def run_stream_checked(cmd, *, cwd=ROOT, must_contain=None, must_not_contain=None):
    print("+", " ".join(map(str, cmd)), flush=True)
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    output = []
    assert proc.stdout is not None
    for line in proc.stdout:
        print(line, end="", flush=True)
        output.append(line)
    rc = proc.wait()
    text = "".join(output)
    if rc != 0:
        raise subprocess.CalledProcessError(rc, cmd)
    if must_contain and must_contain not in text:
        raise RuntimeError(f"command completed but did not emit required marker: {must_contain}")
    if must_not_contain and must_not_contain in text:
        raise RuntimeError(f"command emitted failure marker: {must_not_contain}")
    return text


def ensure_file(path: Path, desc: str):
    if not path.exists():
        raise FileNotFoundError(f"{desc} not found: {path}")


def prepare_payload():
    ensure_file(FW, "firmware image")
    ensure_file(SEVENZ, "7-Zip")

    if PAYLOAD.exists():
        shutil.rmtree(PAYLOAD)
    PAYLOAD.mkdir(parents=True)

    run(["tar", "-xf", str(FW), "-C", str(PAYLOAD)])

    # 1.19.1.126 is an upgrade payload (DEPEND_FW_VERSION=1.17.0.0000) and
    # intentionally omits the immutable Debian base layer.  Reuse the retained
    # 1.17 base layer that this upgrade declares as its dependency.
    base_rootfs = PAYLOAD / "rootfs-base.squashfs"
    if not base_rootfs.exists():
        fallback = ANALYSIS / "rootfs-base.squashfs"
        ensure_file(fallback, "1.17 dependency rootfs-base.squashfs")
        shutil.copy2(fallback, base_rootfs)

    # Pull a monolithic GRUB EFI binary from the base rootfs so the DD image
    # can boot as a removable UEFI disk without needing grub-install.
    run([
        str(SEVENZ),
        "e",
        str(PAYLOAD / "rootfs-base.squashfs"),
        f"-o{PAYLOAD}",
        "-y",
        "usr/lib/grub/x86_64-efi/monolithic/grubx64.efi",
    ])
    ensure_file(PAYLOAD / "grubx64.efi", "extracted grubx64.efi")
    prepare_grub_pc_payload()


def extract_ar_member(path: Path, prefix: bytes) -> bytes:
    data = path.read_bytes()
    if not data.startswith(b"!<arch>\n"):
        raise RuntimeError(f"not an ar archive: {path}")
    pos = 8
    while pos + 60 <= len(data):
        header = data[pos:pos + 60]
        pos += 60
        name = header[:16].decode("ascii", "replace").strip().rstrip("/")
        size = int(header[48:58].decode("ascii").strip())
        body = data[pos:pos + size]
        pos += size + (size % 2)
        if name.encode().startswith(prefix):
            return body
    raise RuntimeError(f"missing {prefix.decode()} member in {path}")


def prepare_grub_pc_payload():
    if not GRUB_PC_DEB.exists():
        GRUB_PC_DEB.parent.mkdir(parents=True, exist_ok=True)
        print(f"+ download {GRUB_PC_URL}", flush=True)
        urllib.request.urlretrieve(GRUB_PC_URL, GRUB_PC_DEB)

    data_tar_xz = extract_ar_member(GRUB_PC_DEB, b"data.tar")
    source = tarfile.open(fileobj=io.BytesIO(data_tar_xz), mode="r:*")
    dest_path = PAYLOAD / "grub-pc-bin.tar"
    if dest_path.exists():
        dest_path.unlink()
    try:
        with tarfile.open(dest_path, "w") as dest:
            copied = 0
            for member in source.getmembers():
                name = member.name
                while name.startswith("./"):
                    name = name[2:]
                if name == "usr/lib/grub/i386-pc" or name.startswith("usr/lib/grub/i386-pc/"):
                    member.name = name
                    body = None if member.isdir() else source.extractfile(member)
                    dest.addfile(member, body)
                    copied += 1
            if copied == 0:
                raise RuntimeError("grub-pc-bin did not contain i386-pc GRUB files")
    finally:
        source.close()
    ensure_file(dest_path, "grub-pc-bin payload")


def build_source_iso():
    import pycdlib

    OUT.mkdir(parents=True, exist_ok=True)
    if SOURCE_ISO.exists():
        SOURCE_ISO.unlink()

    iso_names = {
        "apt.squashfs": "APT.SQF",
        "config.txt": "CONFIG.TXT",
        "fw.squashfs": "FW.SQF",
        "grubx64.efi": "GRUBX64.EFI",
        "grub-pc-bin.tar": "GRUBPC.TAR",
        "initrd.img": "INITRD.IMG",
        "kernel.squashfs": "KERNEL.SQF",
        "md5sum.txt": "MD5SUM.TXT",
        "oem.squashfs": "OEM.SQF",
        "os-release": "OSREL.TXT",
        "rootfs-base.squashfs": "ROOTFS.SQF",
        "ugospro-upgrade": "UGUPGRD",
        "ugpt": "UGPT",
        "ugreen-os-release.json": "UGOSREL.JSN",
        "ugreen.arch": "UGARCH",
        "ugreen.bz2": "UGREEN.BZ2",
        "ugreen.txt": "UGREEN.TXT",
        "ugupdate": "UGUPDATE",
        "version.txt": "VERSION.TXT",
        "vmlinuz": "VMLINUX",
    }

    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, rock_ridge="1.09", vol_ident="UGOS_PAYLOAD")
    try:
        for filename, iso_name in iso_names.items():
            src = PAYLOAD / filename
            ensure_file(src, f"payload file {filename}")
            iso.add_file(
                str(src),
                iso_path=f"/{iso_name};1",
                rr_name=filename,
                joliet_path=f"/{filename}",
            )
        iso.write(str(SOURCE_ISO))
    finally:
        iso.close()
    ensure_file(SOURCE_ISO, "source payload ISO")


def read_newc_entries(cpio_path: Path):
    data = cpio_path.read_bytes()
    pos = 0
    entries = []
    while pos < len(data):
        hdr = data[pos:pos + 110]
        if len(hdr) < 110 or hdr[:6] not in (b"070701", b"070702"):
            raise RuntimeError(f"bad cpio header at {pos}")
        pos += 110
        vals = [int(hdr[6 + i * 8:14 + i * 8], 16) for i in range(13)]
        namesize = vals[11]
        filesize = vals[6]
        name = data[pos:pos + namesize - 1].decode("utf-8", "replace")
        pos += namesize
        pos += (-pos) % 4
        body = data[pos:pos + filesize]
        pos += filesize
        pos += (-pos) % 4
        if name == "TRAILER!!!":
            break
        entries.append((name, vals, body))
    return entries


def newc_header(name: str, mode: int, body: bytes = b"", ino: int = 1) -> bytes:
    namesize = len(name.encode()) + 1
    fields = [
        ino,
        mode,
        0,
        0,
        1,
        int(time.time()),
        len(body),
        0,
        0,
        0,
        0,
        namesize,
        0,
    ]
    return b"070701" + b"".join(f"{x:08x}".encode() for x in fields)


def write_entry(out, name: str, mode: int, body: bytes = b"", ino: int = 1):
    header = newc_header(name, mode, body, ino)
    out.write(header)
    out.write(name.encode() + b"\0")
    out.write(b"\0" * ((4 - ((len(header) + len(name) + 1) % 4)) % 4))
    out.write(body)
    out.write(b"\0" * ((4 - (len(body) % 4)) % 4))


BUILDER_INIT = r"""#!/bin/sh
PATH=/sbin:/usr/sbin:/bin:/usr/bin
export PATH

log() {
  echo "[ugos-dd-builder] $*" >/dev/console
}

fail() {
  log "FAILED: $*"
  sync
  poweroff -f
  halt -f
  reboot -f
}

run() {
  log "+ $*"
  "$@" || fail "$*"
}

mkdir -p /proc /sys /dev /dev/pts /tmp /src /mnt/boot /mnt/root /mnt/rootb /mnt/factory /mnt/ugreen /mnt/overlay /rootfs/base
mount -t proc proc /proc || true
mount -t sysfs sysfs /sys || true
mount -t devtmpfs devtmpfs /dev || true
mkdir -p /dev/pts /tmp /src /mnt/boot /mnt/root /mnt/rootb /mnt/factory /mnt/ugreen /mnt/overlay /rootfs/base
mount -t devpts devpts /dev/pts || true

log "loading modules"
for m in virtio_pci virtio_blk virtio_scsi scsi_mod sd_mod ahci ata_piix libata cdrom isofs vfat fat ext4 squashfs overlay loop; do
  modprobe "$m" >/dev/null 2>&1 || true
done
mdev -s >/dev/null 2>&1 || true
sleep 2

TARGET=/dev/vda
[ -b "$TARGET" ] || TARGET=/dev/sda
[ -b "$TARGET" ] || fail "target disk not found"
log "target disk: $TARGET"

SRCDEV=""
for d in /dev/vdb /dev/vdb1 /dev/sdb /dev/sdb1 /dev/hdb /dev/hdb1 /dev/sr0 /dev/cdrom; do
  if [ -b "$d" ]; then
    if mount -t iso9660 -o ro "$d" /src >/dev/null 2>&1; then
      SRCDEV="$d"
      break
    fi
    if mount -t vfat -o ro "$d" /src >/dev/null 2>&1; then
      SRCDEV="$d"
      break
    fi
  fi
done
[ -n "$SRCDEV" ] || fail "source vvfat disk not found"
log "source disk: $SRCDEV"

for f in vmlinuz initrd.img rootfs-base.squashfs kernel.squashfs fw.squashfs apt.squashfs oem.squashfs ugreen-os-release.json ugreen.bz2 grubx64.efi grub-pc-bin.tar; do
  [ -f "/src/$f" ] || fail "missing /src/$f"
done

log "reading prebuilt GPT partition table"
partprobe "$TARGET" >/dev/null 2>&1 || true
blockdev --rereadpt "$TARGET" >/dev/null 2>&1 || true
mdev -s >/dev/null 2>&1 || true
sleep 3

P1=${TARGET}1
P2=${TARGET}2
P3=${TARGET}3
P4=${TARGET}4
P5=${TARGET}5
P6=${TARGET}6
P7=${TARGET}7
for p in "$P1" "$P2" "$P3" "$P4" "$P5" "$P6" "$P7"; do
  [ -b "$p" ] || fail "partition not found: $p"
done

log "formatting filesystems"
run mkdosfs -F 32 -n EFI "$P1"
run mkfs.ext4 -F -L rootfsA "$P2"
run mkfs.ext4 -F -L factory "$P3"
run mkfs.ext4 -F -L rootfsB "$P4"
run mkfs.ext4 -F -L reserved "$P5"
run mkfs.ext4 -F -L ugreen "$P6"
run mkfs.ext4 -F -L USER-DATA "$P7"

ROOT_PARTUUID=$(blkid "$P2" | sed -n 's/.*PARTUUID="\([^"]*\)".*/\1/p')
[ -n "$ROOT_PARTUUID" ] || fail "cannot read PARTUUID for $P2"
log "root PARTUUID: $ROOT_PARTUUID"
BOOT_UUID=$(blkid -s UUID -o value "$P1" 2>/dev/null || true)
[ -n "$BOOT_UUID" ] || fail "cannot read UUID for $P1"
log "ESP UUID: $BOOT_UUID"

log "installing ESP"
run mount -t vfat "$P1" /mnt/boot
mkdir -p /mnt/boot/EFI/BOOT /mnt/boot/EFI/debian /mnt/boot/boot /mnt/boot/boot/grub
cp /src/grubx64.efi /mnt/boot/EFI/BOOT/BOOTX64.EFI || fail "copy BOOTX64.EFI"
cp /src/grubx64.efi /mnt/boot/EFI/debian/grubx64.efi || fail "copy grubx64.efi"
cp /src/vmlinuz /mnt/boot/boot/vmlinuz || fail "copy vmlinuz"
cp /src/initrd.img /mnt/boot/boot/initrd.img || fail "copy initrd"
cat >/mnt/boot/EFI/debian/grub.cfg <<EOF
set timeout=3
set default=0
terminal_output console

menuentry 'UGOS Pro 1.19.1.126' {
    linux /boot/vmlinuz root=PARTUUID=$ROOT_PARTUUID rw net.ifnames=0 biosdevname=0 console=tty0 console=ttyS0,115200
    initrd /boot/initrd.img
}

menuentry 'UGOS Pro 1.19.1.126 (serial debug)' {
    linux /boot/vmlinuz root=PARTUUID=$ROOT_PARTUUID rw net.ifnames=0 biosdevname=0 console=ttyS0,115200 loglevel=7
    initrd /boot/initrd.img
}
EOF
cat >/mnt/boot/EFI/debian/grub.am <<'EOF'
set timeout=3
set default=0
terminal_output console

menuentry 'UGOS Pro' {
    linux /boot/@VMLINUXZ@ root=PARTUUID=@PART2UUID@ rw net.ifnames=0 biosdevname=0 console=tty0 console=ttyS0,115200
    initrd /boot/@INITRDIMG@
}
EOF
cp /mnt/boot/EFI/debian/grub.cfg /mnt/boot/EFI/BOOT/grub.cfg || fail "copy fallback grub.cfg"
cp /mnt/boot/EFI/debian/grub.cfg /mnt/boot/boot/grub/grub.cfg || fail "copy boot grub.cfg"

log "installing BIOS GRUB"
mkdir -p /tmp/grub-pc /rootfs/base
tar -xf /src/grub-pc-bin.tar -C /tmp/grub-pc || fail "extract grub-pc-bin.tar"
chmod -R u+rwX,go+rX /tmp/grub-pc || true
run mount -t squashfs -o loop,ro /src/rootfs-base.squashfs /rootfs/base
ROOTFS_LD=/rootfs/base/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
ROOTFS_LIB=/rootfs/base/usr/lib/x86_64-linux-gnu:/rootfs/base/lib/x86_64-linux-gnu:/rootfs/base/lib:/rootfs/base/usr/lib
GRUB_I386=/tmp/grub-pc/usr/lib/grub/i386-pc
chmod 755 "$GRUB_I386/grub-bios-setup" 2>/dev/null || true
[ -x "$ROOTFS_LD" ] || fail "missing rootfs dynamic loader"
[ -x /rootfs/base/usr/bin/grub-mkimage ] || fail "missing grub-mkimage"
[ -x "$GRUB_I386/grub-bios-setup" ] || fail "missing grub-bios-setup"
cat >/tmp/grub-bios-early.cfg <<EOF
set timeout=0
terminal_output console
search --no-floppy --fs-uuid --set=root $BOOT_UUID
linux /boot/vmlinuz root=PARTUUID=$ROOT_PARTUUID rw net.ifnames=0 biosdevname=0 console=tty0 console=ttyS0,115200
initrd /boot/initrd.img
boot
EOF
run "$ROOTFS_LD" --library-path "$ROOTFS_LIB" /rootfs/base/usr/bin/grub-mkimage \
  -O i386-pc \
  -d "$GRUB_I386" \
  -p /boot/grub \
  -c /tmp/grub-bios-early.cfg \
  -o /tmp/core.img \
  biosdisk part_gpt fat search search_fs_uuid linux boot
cp /tmp/core.img "$GRUB_I386/core.img" || fail "stage BIOS core.img"
cat >/tmp/device.map <<EOF
(hd0) $TARGET
EOF
run "$ROOTFS_LD" --library-path "$ROOTFS_LIB" "$GRUB_I386/grub-bios-setup" \
  -d "$GRUB_I386" \
  -m /tmp/device.map \
  -b boot.img \
  -c core.img \
  "$TARGET"
umount /rootfs/base || true

log "installing rootfs slot A"
run mount -t ext4 "$P2" /mnt/root
for d in base kernel apt fw oem; do mkdir -p "/mnt/root/$d"; done
for f in rootfs-base.squashfs kernel.squashfs fw.squashfs apt.squashfs oem.squashfs ugreen-os-release.json; do
  cp "/src/$f" "/mnt/root/$f" || fail "copy $f"
done

log "preparing rootfs slot B"
run mount -t ext4 "$P4" /mnt/rootb
for d in base kernel apt fw oem; do mkdir -p "/mnt/rootb/$d"; done
cp /src/ugreen-os-release.json /mnt/rootb/ugreen-os-release.json || true

log "preparing factory and overlay"
run mount -t ext4 "$P3" /mnt/factory
cp /src/md5sum.txt /mnt/factory/md5sum.txt 2>/dev/null || true
run mount -t ext4 "$P7" /mnt/overlay
mkdir -p /mnt/overlay/upper /mnt/overlay/work

log "installing universal VPS/bare-metal compatibility layer"
mkdir -p \
  /mnt/overlay/upper/usr/local/sbin \
  /mnt/overlay/upper/usr/local/lib/ugos-universal \
  /mnt/overlay/upper/etc/systemd/system/sysinit.target.wants \
  /mnt/overlay/upper/etc/systemd/system/multi-user.target.wants \
  /mnt/overlay/upper/etc/systemd/system/storage_serv.service.d \
  /mnt/overlay/upper/etc/nginx/conf.d \
  /mnt/overlay/upper/etc/ugos-universal

cat > /mnt/overlay/upper/usr/local/lib/ugos-universal/smbios_spoof.py <<'PYEOF'
from pathlib import Path
import os

base = Path("/etc/ugos-universal/smbios")
base.mkdir(parents=True, exist_ok=True)
dmi_path = Path("/sys/firmware/dmi/tables/DMI")
ep_path = Path("/sys/firmware/dmi/tables/smbios_entry_point")

model = os.environ.get("UGOS_MODEL", "DXP6800 Pro")
serial = os.environ.get("UGOS_SN", "EE720JJ000000001")
sku = os.environ.get("UGOS_SKU", "DXP6800PRO")
family = os.environ.get("UGOS_FAMILY", "gray")

orig_dmi = dmi_path.read_bytes()
orig_ep = ep_path.read_bytes()
if not (base / "original.DMI").exists():
    (base / "original.DMI").write_bytes(orig_dmi)
if not (base / "original.smbios_entry_point").exists():
    (base / "original.smbios_entry_point").write_bytes(orig_ep)

def split_structs(data):
    out = []
    i = 0
    while i + 4 <= len(data):
        typ = data[i]
        ln = data[i + 1]
        if ln < 4 or i + ln > len(data):
            raise RuntimeError(f"bad SMBIOS structure at {i}")
        header = bytearray(data[i:i + ln])
        j = i + ln
        start = j
        while j + 1 < len(data):
            if data[j] == 0 and data[j + 1] == 0:
                raw = data[start:j]
                strings = [s.decode("latin1", "replace") for s in raw.split(b"\0") if s] if raw else []
                j += 2
                break
            j += 1
        else:
            raise RuntimeError("unterminated SMBIOS string area")
        out.append((typ, header, strings))
        i = j
    return out

def pack(header, strings):
    # Every SMBIOS structure ends with a double NUL.  Building the payload by
    # joining first also handles structures with no strings (notably type 127),
    # which still require two terminator bytes.
    body = b"\0".join(s.encode("latin1", "replace") for s in strings) + b"\0\0"
    return bytes(header) + body

new = []
for typ, h, strings in split_structs(orig_dmi):
    if typ == 0 and len(h) >= 9:
        strings = ["American Megatrends International, LLC.", "5.27", "06/26/2026"]
        h[4] = 1
        h[5] = 2
        h[8] = 3
    elif typ == 1 and len(h) >= 27:
        strings = ["UGREEN", model, "1.0", serial, sku, family]
        h[4] = 1
        h[5] = 2
        h[6] = 3
        h[7] = 4
        h[25] = 5
        h[26] = 6
    elif typ == 2 and len(h) >= 8:
        strings = ["UGREEN", model, "1.0", serial]
        h[4] = 1
        h[5] = 2
        h[6] = 3
        h[7] = 4
    elif typ == 3 and len(h) >= 9:
        strings = ["UGREEN", model, serial, "UGREEN NAS"]
        h[4] = 1
        h[5] = 0x03
        h[6] = 2
        h[7] = 3
        h[8] = 4
    new.append(pack(h, strings))

new_dmi = b"".join(new)
new_ep = bytearray(orig_ep)
if len(new_ep) >= 0x1F and new_ep[0:4] == b"_SM_" and new_ep[0x10:0x15] == b"_DMI_":
    new_ep[0x16:0x18] = len(new_dmi).to_bytes(2, "little")
    max_len = max(len(pack(h, strings)) for _, h, strings in split_structs(new_dmi))
    new_ep[0x08:0x0A] = min(max_len, 0xFFFF).to_bytes(2, "little")
    new_ep[0x15] = 0
    new_ep[0x15] = (-sum(new_ep[0x10:0x1F])) & 0xFF
    ep_len = new_ep[0x05]
    new_ep[0x04] = 0
    new_ep[0x04] = (-sum(new_ep[:ep_len])) & 0xFF
else:
    raise RuntimeError("unsupported SMBIOS entry point")

(base / "DMI").write_bytes(new_dmi)
(base / "smbios_entry_point").write_bytes(bytes(new_ep))
PYEOF

cat > /mnt/overlay/upper/usr/local/sbin/ugos-universal-hw-init.sh <<'EOF'
#!/bin/sh
set -eu

BASE=/etc/ugos-universal
IDENT="$BASE/identity.env"
DMI="$BASE/dmi"
MODEL=${UGOS_MODEL:-"DXP6800 Pro"}
SKU=${UGOS_SKU:-"DXP6800PRO"}
FAMILY=${UGOS_FAMILY:-"gray"}

mkdir -p "$BASE" "$DMI" /tmp/factory /tmp/.cache /tmp/.nas

if [ ! -f "$IDENT" ]; then
  seed="$(cat /etc/machine-id 2>/dev/null || true)"
  [ -n "$seed" ] || seed="$(cat /proc/sys/kernel/random/uuid 2>/dev/null || date +%s%N)"
  macs="$(cat /sys/class/net/*/address 2>/dev/null | tr -d ':\n' || true)"
  hash="$(printf '%s' "$seed$macs" | sha256sum | awk '{print $1}')"
  n=$((0x$(printf '%s' "$hash" | cut -c1-8) % 1000000000))
  uuid="$(cat /proc/sys/kernel/random/uuid 2>/dev/null || printf '%s-%s-%s-%s-%s\n' "${hash%????????????????????????????}" "$(printf '%s' "$hash" | cut -c9-12)" "$(printf '%s' "$hash" | cut -c13-16)" "$(printf '%s' "$hash" | cut -c17-20)" "$(printf '%s' "$hash" | cut -c21-32)")"
  {
    # identity.env is sourced by multiple boot helpers.  Quote every value so
    # model names containing spaces (for example "DXP6800 Pro") remain one
    # shell assignment instead of aborting the early boot service.
    printf "UGOS_MODEL='%s'\n" "$MODEL"
    printf "UGOS_SKU='%s'\n" "$SKU"
    printf "UGOS_FAMILY='%s'\n" "$FAMILY"
    printf "UGOS_SN='EE720JJ%09d'\n" "$n"
    printf "UGOS_UUID='%s'\n" "$uuid"
  } > "$IDENT"
  chmod 600 "$IDENT"
fi

. "$IDENT"

write_dmi() {
  printf '%s\n' "$2" > "$DMI/$1"
}

write_dmi sys_vendor UGREEN
write_dmi product_name "$UGOS_MODEL"
write_dmi product_version "1.0"
write_dmi product_serial "$UGOS_SN"
write_dmi product_sku "$UGOS_SKU"
write_dmi product_family "$UGOS_FAMILY"
write_dmi board_vendor UGREEN
write_dmi board_name "$UGOS_MODEL"
write_dmi board_version "1.0"
write_dmi board_serial "$UGOS_SN"
write_dmi chassis_vendor UGREEN
write_dmi chassis_type 3
write_dmi chassis_version "1.0"
write_dmi chassis_serial "$UGOS_SN"
write_dmi bios_vendor "American Megatrends International, LLC."
write_dmi bios_version "5.27"
write_dmi bios_date "06/26/2026"

for f in sys_vendor product_name product_version product_serial product_sku product_family board_vendor board_name board_version board_serial chassis_vendor chassis_type chassis_version chassis_serial bios_vendor bios_version bios_date; do
  [ -e "/sys/class/dmi/id/$f" ] || continue
  mountpoint -q "/sys/class/dmi/id/$f" 2>/dev/null && continue
  mount --bind "$DMI/$f" "/sys/class/dmi/id/$f" 2>/dev/null || true
done

if [ -r /sys/firmware/dmi/tables/DMI ] && [ -r /sys/firmware/dmi/tables/smbios_entry_point ]; then
  UGOS_MODEL="$UGOS_MODEL" UGOS_SN="$UGOS_SN" UGOS_SKU="$UGOS_SKU" UGOS_FAMILY="$UGOS_FAMILY" \
    python3 /usr/local/lib/ugos-universal/smbios_spoof.py 2>/dev/null || true
  for f in DMI smbios_entry_point; do
    [ -f "$BASE/smbios/$f" ] || continue
    [ -e "/sys/firmware/dmi/tables/$f" ] || continue
    mountpoint -q "/sys/firmware/dmi/tables/$f" 2>/dev/null && continue
    mount --bind "$BASE/smbios/$f" "/sys/firmware/dmi/tables/$f" 2>/dev/null || true
  done
fi

printf '63\n' > /tmp/.nas/sata_sw
printf '%s\n' "$UGOS_MODEL" > /tmp/factory/model.txt
printf '%s\n' "$UGOS_SN" > /tmp/factory/sn.txt
# ctlmgr falls back to this same built-in key when the hardware pull helper
# cannot provide one, but its setup wizard also requires the marker file.
printf '%s\n' 'UGN123NAS@#$' > /tmp/factory/activation_key.txt
chmod 600 /tmp/factory/activation_key.txt

cat > /tmp/.cache/.board_cache <<JSON
{"manufacturer":"UGREEN","product_name":"${UGOS_MODEL}","bios_version":"5.27","serial_number":"${UGOS_SN}","uuid":"${UGOS_UUID}","wakeup_type":"Power Switch","sku_number":"${UGOS_SKU}","color":"${UGOS_FAMILY}"}
JSON

cat > /etc/led.build <<JSON
[led]
json = {"info":[{"days":[7,6],"timeConfig":[{"time":[],"bright":100}]},{"days":[1,2,3,4,5],"timeConfig":[{"time":[],"bright":100}]}],"model":"${UGOS_MODEL}","status":1}
JSON
EOF

cat > /mnt/overlay/upper/usr/local/sbin/ugos-universal-expand-overlay.sh <<'EOF'
#!/bin/sh
set -eu

STATE=/etc/ugos-universal/overlay-expanded
[ -f "$STATE" ] && exit 0

src="$(findmnt -n -o SOURCE /overlay 2>/dev/null || true)"
[ -n "$src" ] || src="$(findmnt -n -o SOURCE / 2>/dev/null || true)"
case "$src" in
  /dev/*[0-9]) ;;
  *) exit 0 ;;
esac

part="$src"
pk="$(lsblk -no PKNAME "$part" 2>/dev/null | head -1 || true)"
[ -n "$pk" ] || exit 0
disk="/dev/$pk"
num="$(lsblk -no PARTN "$part" 2>/dev/null | head -1 || true)"
[ "$num" = "7" ] || exit 0

node="${part##*/}"
sys_part="/sys/class/block/$node"
[ -r "$sys_part/start" ] && [ -r "$sys_part/size" ] || exit 1
start="$(cat "$sys_part/start")"
size_before="$(cat "$sys_part/size")"
disk_sectors="$(blockdev --getsz "$disk")"

# A raw 16 GiB image leaves its backup GPT and USER-DATA end at the source
# image boundary.  On a larger target, relocate the backup GPT and grow the
# final partition.  parted -f handles the misplaced backup GPT; keep sgdisk as
# a fallback for minimal installations.
remaining=$((disk_sectors - start - size_before))
if [ "$remaining" -gt 4096 ]; then
  expanded=0
  if command -v parted >/dev/null 2>&1; then
    parted -s -f "$disk" resizepart 7 100% >/dev/null 2>&1 && expanded=1
  fi
  if [ "$expanded" -eq 0 ] && command -v sgdisk >/dev/null 2>&1; then
    sgdisk -e "$disk" >/dev/null 2>&1 && \
      sgdisk -d 7 -n "7:${start}:0" -c 7:USER-DATA -t 7:8300 "$disk" >/dev/null 2>&1 && expanded=1
  fi
  [ "$expanded" -eq 1 ] || exit 1
  partprobe "$disk" >/dev/null 2>&1 || true
  blockdev --rereadpt "$disk" >/dev/null 2>&1 || true
  udevadm settle >/dev/null 2>&1 || true
  size_after="$(cat "$sys_part/size")"
  [ "$size_after" -gt "$size_before" ] || exit 1
fi

resize2fs "$part" >/dev/null 2>&1
date > "$STATE"
EOF

cat > /mnt/overlay/upper/usr/local/sbin/ugos-universal-storage-patch.sh <<'EOF'
#!/bin/sh
set -eu

BIN=/ugreen/@appstore/com.ugreen.storagemgr/sbin/storage_serv
STATE=/etc/ugos-universal/storage
mkdir -p "$STATE" /tmp/.nas
printf '63\n' > /tmp/.nas/sata_sw
[ -f "$BIN" ] || exit 0

if [ ! -f "$STATE/storage_serv.initial.bak" ]; then
  cp -a "$BIN" "$STATE/storage_serv.initial.bak"
fi

if LC_ALL=C grep -aq '/proc/nas/sata_sw' "$BIN"; then
  cp -a "$BIN" "$STATE/storage_serv.before_sata_sw_patch.$(date +%Y%m%d%H%M%S).bak"
  perl -0pi -e 's|\Q/proc/nas/sata_sw\E|/tmp/.nas/sata_sw|g' "$BIN"
fi

# storage_serv 1.19.1.126 identifies internal bays from the real /sys/block
# path.  Our one-disk VPS data device is backed by tcm_loop and therefore has
# /devices/virtual/ in that path; without a matching bay rule UGOS classifies
# it as external USB and refuses to create a pool.  Change only the first SATA
# bay rule for the DXP6800 Plus/Pro hardware table from /ata3/ to /virtual/.
# The exact original bytes are verified before the version-specific edit, so a
# later firmware cannot receive this patch accidentally.
perl -0777pi -e '
  $off = 0x17d56d0;
  $from = pack("H*", "31879301000000000400000000000000A9F79301000000000600000000000000C5879301000000000400000000000000");
  $to   = pack("H*", "31879301000000000400000000000000A9F79301000000000600000000000000A8D09501000000000700000000000000");
  $got = substr($_, $off, length($from));
  if ($got eq $from) {
    substr($_, $off, length($from), $to);
  } elsif ($got ne $to) {
    die "unsupported storage_serv layout; refusing virtual-bay patch\n";
  }
' "$BIN"

chmod 755 "$BIN"
EOF

cat > /mnt/overlay/upper/usr/local/sbin/ugos-universal-virtual-data-disk.sh <<'EOF'
#!/bin/sh
set -eu

CFG=/etc/ugos-universal/identity.env
[ -f "$CFG" ] && . "$CFG" || true

root_src="$(findmnt -n -o SOURCE /overlay 2>/dev/null || findmnt -n -o SOURCE / 2>/dev/null || true)"
root_pk=""
if [ -n "$root_src" ]; then
  root_pk="$(lsblk -no PKNAME "$root_src" 2>/dev/null | head -1 || true)"
fi

real_data_disk=0
for d in /sys/block/*; do
  name="${d##*/}"
  case "$name" in loop*|ram*|zram*|sr*|fd*|dm-*|md*) continue ;; esac
  [ "$name" = "$root_pk" ] && continue
  [ "$(cat "$d/ro" 2>/dev/null || echo 1)" = 0 ] || continue
  bytes="$(blockdev --getsize64 "/dev/$name" 2>/dev/null || echo 0)"
  [ "$bytes" -ge $((32 * 1024 * 1024 * 1024)) ] || continue
  real_data_disk=1
done

# If a real extra disk exists, leave storage to UGOS. If there is only the boot
# disk, expose part of USER-DATA as a virtual HDD so one-disk VPS installs can
# create a storage pool.
[ "$real_data_disk" = 0 ] || exit 0

IMG=/overlay/virtual-disks/ugos-data0.img
BACKSTORE=/sys/kernel/config/target/core/iblock_0/ugos_data0
TARGET=/sys/kernel/config/target/loopback/naa.5001405ugosdata0
INITIATOR=naa.5001405ugosinit0

mkdir -p /overlay/virtual-disks
if [ ! -f "$IMG" ]; then
  avail_kb="$(df -Pk /overlay | awk 'NR==2 {print $4}')"
  reserve_kb=$((8 * 1024 * 1024))
  if [ "$avail_kb" -le "$reserve_kb" ]; then
    exit 0
  fi
  size_mb=$(((avail_kb - reserve_kb) * 85 / 100 / 1024))
  [ "$size_mb" -ge 32768 ] || exit 0
  truncate -s "${size_mb}M" "$IMG"
fi

modprobe loop || true
modprobe configfs || true
modprobe target_core_mod || true
modprobe target_core_iblock || true
modprobe tcm_loop || true
mountpoint -q /sys/kernel/config || mount -t configfs configfs /sys/kernel/config || true

LOOP="$(losetup -j "$IMG" | sed -n 's/^\([^:]*\):.*/\1/p' | head -1)"
if [ -z "$LOOP" ]; then
  LOOP="$(losetup --find --show "$IMG")"
fi

if [ ! -d "$BACKSTORE" ]; then
  mkdir -p "$BACKSTORE"
  [ -w "$BACKSTORE/wwn/vendor_id" ] && echo UGREEN > "$BACKSTORE/wwn/vendor_id" 2>/dev/null || true
  [ -w "$BACKSTORE/wwn/product_id" ] && echo DXP6800DATA > "$BACKSTORE/wwn/product_id" 2>/dev/null || true
  [ -w "$BACKSTORE/wwn/revision" ] && echo 1.0 > "$BACKSTORE/wwn/revision" 2>/dev/null || true
  [ -w "$BACKSTORE/wwn/vpd_unit_serial" ] && echo "UGOSDATA${UGOS_SN:-000000000}" > "$BACKSTORE/wwn/vpd_unit_serial" 2>/dev/null || true
  echo "udev_path=$LOOP" > "$BACKSTORE/control"
  echo 1 > "$BACKSTORE/enable"
elif [ -f "$BACKSTORE/enable" ]; then
  [ "$(cat "$BACKSTORE/enable" 2>/dev/null || echo 0)" = 1 ] || echo 1 > "$BACKSTORE/enable" || true
fi

mkdir -p "$TARGET/tpgt_1/lun/lun_0"
if [ -f "$TARGET/tpgt_1/nexus" ]; then
  nexus="$(cat "$TARGET/tpgt_1/nexus" 2>/dev/null || true)"
  [ -n "$nexus" ] || echo "$INITIATOR" > "$TARGET/tpgt_1/nexus" || true
fi
if ! find "$TARGET/tpgt_1/lun/lun_0" -maxdepth 1 -type l | grep -q . 2>/dev/null; then
  ln -s "$BACKSTORE" "$TARGET/tpgt_1/lun/lun_0/ugos_data0" 2>/dev/null || true
fi

for host in /sys/class/scsi_host/host*; do
  real="$(readlink -f "$host" 2>/dev/null || true)"
  case "$real" in *tcm_loop*) echo '- - -' > "$host/scan" 2>/dev/null || true ;; esac
done
udevadm settle 2>/dev/null || true
EOF

chmod 755 \
  /mnt/overlay/upper/usr/local/sbin/ugos-universal-hw-init.sh \
  /mnt/overlay/upper/usr/local/sbin/ugos-universal-expand-overlay.sh \
  /mnt/overlay/upper/usr/local/sbin/ugos-universal-storage-patch.sh \
  /mnt/overlay/upper/usr/local/sbin/ugos-universal-virtual-data-disk.sh

# Generic x86 machines have no UGREEN factory-cloud production record.  The
# local readiness endpoint reports that condition as status 2 even when all
# identity fields are present, which prevents the browser setup wizard from
# opening.  Override only this pre-initialization gate; all wizard actions and
# normal control-panel APIs continue to use ctlmgr.
cat > /mnt/overlay/upper/etc/nginx/conf.d/00-ugos-universal-wizard.conf <<'EOF'
location = /ugreen/v1/wizard/_/status {
    default_type application/json;
    add_header Cache-Control "no-store" always;
    return 200 '{"code":200,"msg":"success","data":{"mac":"","name":"","status":1},"time":0}';
}
EOF

cat > /mnt/overlay/upper/etc/systemd/system/ugos-universal-hw-init.service <<'EOF'
[Unit]
Description=UGOS universal hardware identity initialization
DefaultDependencies=no
After=local-fs.target sysinit.target
Before=basic.target

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/ugos-universal-hw-init.sh
RemainAfterExit=yes

[Install]
WantedBy=sysinit.target
EOF

cat > /mnt/overlay/upper/etc/systemd/system/ugos-universal-expand-overlay.service <<'EOF'
[Unit]
Description=Expand UGOS USER-DATA partition to the target disk
After=local-fs.target ugos-universal-hw-init.service
Before=ugos-universal-virtual-data-disk.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/ugos-universal-expand-overlay.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

cat > /mnt/overlay/upper/etc/systemd/system/ugos-universal-storage-patch.service <<'EOF'
[Unit]
Description=Patch UGOS storage service for generic x86 hardware
After=local-fs.target ugos-universal-hw-init.service
Before=storage_serv.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/ugos-universal-storage-patch.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

cat > /mnt/overlay/upper/etc/systemd/system/ugos-universal-virtual-data-disk.service <<'EOF'
[Unit]
Description=Expose boot-disk free space as a UGOS virtual data disk
After=local-fs.target ugos-universal-expand-overlay.service ugos-universal-storage-patch.service
Before=storage_serv.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/ugos-universal-virtual-data-disk.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

cat > /mnt/overlay/upper/etc/systemd/system/storage_serv.service.d/10-ugos-universal.conf <<'EOF'
[Unit]
Requires=ugos-universal-storage-patch.service ugos-universal-virtual-data-disk.service
After=ugos-universal-storage-patch.service ugos-universal-virtual-data-disk.service
EOF

ln -sf ../ugos-universal-hw-init.service /mnt/overlay/upper/etc/systemd/system/sysinit.target.wants/ugos-universal-hw-init.service
ln -sf ../ugos-universal-expand-overlay.service /mnt/overlay/upper/etc/systemd/system/multi-user.target.wants/ugos-universal-expand-overlay.service
ln -sf ../ugos-universal-storage-patch.service /mnt/overlay/upper/etc/systemd/system/multi-user.target.wants/ugos-universal-storage-patch.service
ln -sf ../ugos-universal-virtual-data-disk.service /mnt/overlay/upper/etc/systemd/system/multi-user.target.wants/ugos-universal-virtual-data-disk.service

log "installing /ugreen payload"
run mount -t ext4 "$P6" /mnt/ugreen
tar -xf /src/ugreen.bz2 -C /mnt/ugreen || fail "extract ugreen.bz2"
cp /src/ugreen.txt /mnt/ugreen/.ugreen.txt 2>/dev/null || true

log "syncing"
sync
umount /mnt/ugreen || true
umount /mnt/overlay || true
umount /mnt/factory || true
umount /mnt/rootb || true
umount /mnt/root || true
umount /mnt/boot || true
umount /rootfs/base || true
umount /src || true
sync
log "DONE"
poweroff -f
halt -f
reboot -f
"""


def build_initrd():
    ensure_file(ANALYSIS / "initrd.cpio", "decompressed initrd.cpio")
    entries = read_newc_entries(ANALYSIS / "initrd.cpio")
    with BUILDER_CPIO.open("wb") as out:
        ino = 1
        for name, vals, body in entries:
            if name == "init":
                continue
            mode = vals[1]
            write_entry(out, name, mode, body, ino)
            ino += 1
        write_entry(out, "init", 0o100755, BUILDER_INIT.encode("utf-8"), ino)
        write_entry(out, "TRAILER!!!", 0, b"", ino + 1)
    run(["zstd", "-f", str(BUILDER_CPIO), "-o", str(BUILDER_INITRD)])


def create_image():
    ensure_file(QEMU, "QEMU")
    ensure_file(QEMU_IMG, "qemu-img")
    OUT.mkdir(parents=True, exist_ok=True)
    stale_zst = IMAGE.with_suffix(IMAGE.suffix + ".zst")
    if stale_zst.exists():
        stale_zst.unlink()
    if IMAGE.exists():
        IMAGE.unlink()
    run([str(QEMU_IMG), "create", "-f", "raw", str(IMAGE), f"{IMAGE_SIZE_GIB}G"])
    write_gpt_image(IMAGE, IMAGE_SIZE_GIB * 1024**3)


def sectors_for_mib(mib: int) -> int:
    return mib * 1024 * 1024 // 512


def gpt_partition_entry(type_guid: uuid.UUID, first_lba: int, last_lba: int, name: str) -> bytes:
    unique_guid = uuid.uuid4()
    encoded_name = name.encode("utf-16le")[:72].ljust(72, b"\0")
    return (
        type_guid.bytes_le
        + unique_guid.bytes_le
        + struct.pack("<QQQ", first_lba, last_lba, 0)
        + encoded_name
    )


def gpt_header(
    *,
    current_lba: int,
    backup_lba: int,
    first_usable: int,
    last_usable: int,
    disk_guid: uuid.UUID,
    entries_start: int,
    entries_count: int,
    entry_size: int,
    entries_crc: int,
) -> bytes:
    header = (
        b"EFI PART"
        + struct.pack("<IIII", 0x00010000, 92, 0, 0)
        + struct.pack("<QQQQ", current_lba, backup_lba, first_usable, last_usable)
        + disk_guid.bytes_le
        + struct.pack("<QIII", entries_start, entries_count, entry_size, entries_crc)
    )
    header = header[:16] + struct.pack("<I", zlib.crc32(header[:92]) & 0xFFFFFFFF) + header[20:]
    return header.ljust(512, b"\0")


def write_gpt_image(image: Path, size_bytes: int):
    sector_size = 512
    total_sectors = size_bytes // sector_size
    entries_count = 128
    entry_size = 128
    entries_sectors = entries_count * entry_size // sector_size
    first_usable = 2048
    last_usable = total_sectors - 34
    primary_entries_lba = 2
    backup_header_lba = total_sectors - 1
    backup_entries_lba = total_sectors - 1 - entries_sectors

    efi_type = uuid.UUID("c12a7328-f81f-11d2-ba4b-00a0c93ec93b")
    linux_type = uuid.UUID("0fc63daf-8483-4772-8e79-3d69d8477de4")
    bios_type = uuid.UUID("21686148-6449-6e6f-744e-656564454649")

    layout = []
    bios_start = first_usable
    bios_end = bios_start + sectors_for_mib(BIOS_BOOT_PARTITION_MIB) - 1
    start = bios_end + 1
    for name, size_mib, type_guid in [
        ("EFI", 512, efi_type),
        ("rootfsA", 1900, linux_type),
        ("factory", 128, linux_type),
        ("rootfsB", 1900, linux_type),
        ("reserved", 64, linux_type),
        ("ugreen", UGREEN_PARTITION_MIB, linux_type),
    ]:
        sectors = sectors_for_mib(size_mib)
        end = start + sectors - 1
        layout.append((type_guid, start, end, name))
        start = end + 1
    layout.append((linux_type, start, last_usable, "USER-DATA"))
    layout.append((bios_type, bios_start, bios_end, "BIOS-BOOT"))

    entries = b"".join(gpt_partition_entry(*part) for part in layout)
    entries = entries.ljust(entries_count * entry_size, b"\0")
    entries_crc = zlib.crc32(entries) & 0xFFFFFFFF
    disk_guid = uuid.uuid4()

    protective_mbr = bytearray(512)
    protective_mbr[446:462] = (
        b"\x80"
        + b"\0\x02\0"
        + b"\xee"
        + b"\xff\xff\xff"
        + struct.pack("<II", 1, min(total_sectors - 1, 0xFFFFFFFF))
    )
    protective_mbr[510:512] = b"\x55\xaa"

    primary_header = gpt_header(
        current_lba=1,
        backup_lba=backup_header_lba,
        first_usable=first_usable,
        last_usable=last_usable,
        disk_guid=disk_guid,
        entries_start=primary_entries_lba,
        entries_count=entries_count,
        entry_size=entry_size,
        entries_crc=entries_crc,
    )
    backup_header = gpt_header(
        current_lba=backup_header_lba,
        backup_lba=1,
        first_usable=first_usable,
        last_usable=last_usable,
        disk_guid=disk_guid,
        entries_start=backup_entries_lba,
        entries_count=entries_count,
        entry_size=entry_size,
        entries_crc=entries_crc,
    )

    with image.open("r+b") as f:
        f.seek(0)
        f.write(protective_mbr)
        f.seek(sector_size)
        f.write(primary_header)
        f.seek(primary_entries_lba * sector_size)
        f.write(entries)
        f.seek(backup_entries_lba * sector_size)
        f.write(entries)
        f.seek(backup_header_lba * sector_size)
        f.write(backup_header)


def qemu_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/")


def run_builder():
    ensure_file(BUILDER_KERNEL, "builder kernel matching builder initrd modules")
    cmd = [
        str(QEMU),
        "-display", "none",
        "-serial", "stdio",
        "-monitor", "none",
        "-no-reboot",
        "-m", "2048",
        "-machine", "pc,accel=tcg",
        # This kernel is only the image-construction environment.  The target
        # ESP receives PAYLOAD/vmlinuz (the new 6.18 production kernel).
        "-kernel", str(BUILDER_KERNEL.resolve()),
        "-initrd", str(BUILDER_INITRD.resolve()),
        "-append", "console=ttyS0,115200 loglevel=7",
        "-drive", f"file={IMAGE.resolve()},format=raw,if=virtio,cache=unsafe",
        "-drive", f"file={SOURCE_ISO.resolve()},format=raw,if=virtio,readonly=on",
    ]
    run_stream_checked(cmd, must_contain="[ugos-dd-builder] DONE", must_not_contain="[ugos-dd-builder] FAILED")


def compress_image():
    zst = IMAGE.with_suffix(IMAGE.suffix + ".zst")
    if zst.exists():
        zst.unlink()
    run(["zstd", "-T0", "-10", "-f", str(IMAGE), "-o", str(zst)])
    run([str(QEMU_IMG), "info", str(IMAGE)])
    print(f"RAW={IMAGE}")
    print(f"ZST={zst}")


def main():
    prepare_payload()
    build_source_iso()
    build_initrd()
    create_image()
    run_builder()
    compress_image()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
