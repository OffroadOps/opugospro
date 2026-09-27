#!/usr/bin/env python3
"""Generic UGOS Pro ARM64 base-image builder.

Hardware-agnostic base package: one builder, one device profile per board.

Inputs
------
- UGOS ARM payload (rootfs/apt/fw/oem/kernel squashfs, initfs.tar.gz, ugreen.bz2)
  referenced in place -- never moved: default D:/img/UGOS arm/payload
- core-preinstall.tar.gz: default D:/img/UGOS arm/staging/core-preinstall/
- Board device dir (staging/<id>-base/):
    bootloader blob (raw region copied to offset 0, covers SoC boot ROM needs)
    bootfs/Image                      -- arm64 kernel Image
    bootfs/dtb/...                    -- DTBs (profile picks one)
    rootfs-overlay/usr/lib/modules/<ver>/  -- full module tree for that kernel

Flow: patched UGOS initramfs discovers the marked payload partition at boot,
assembles the overlay root from the squashfs layers plus the board module tar,
then hands off to systemd.  Proven on Orange Pi Zero 3 (H618) and OEC-T (RK3566).

Usage
-----
python build-ugos-arm-image.py --profile profiles/radxa-cubie-a5e/profile.json \
    --out-image out/ugos-radxa-cubie-a5e-sd-v1.img
"""
import argparse
import gzip
import importlib.util
import json
import lzma
import subprocess
import sys
import tarfile
import time
from pathlib import Path


SECTOR_SIZE = 512
# Identity constants baked into the zero3-era seed block of the base init patch.
# Every one of them is replaced with profile values before the cpio is written.
ZERO3_SERIAL = "UGOSOPIZERO3DF0D8E2E"
ZERO3_HOSTNAME = "UGOS-OPI-ZERO3"
ZERO3_CPU = "Allwinner H618"
ZERO3_BOARD_NAME = "Orange Pi Zero 3"
ZERO3_BUILD_MARKER = "v18-preinstall-debug"
ZERO3_UUID = "297f42ed-4333-43ea-9400-2cd3ee3e0184"
ZERO3_MAC = "02:00:DF:0D:8E:2E"
DEFAULT_COMPAT_MODEL = "DH4300PLUS"
DEFAULT_MODEL_SERIES = "dh4300plus"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {label}: {path}")


def require_dir(path: Path, label: str) -> None:
    if not path.is_dir():
        raise NotADirectoryError(f"Missing {label}: {path}")


def load_profile(path: Path) -> dict:
    profile = json.loads(path.read_text(encoding="utf-8"))
    for key in ("id", "display_name", "hostname", "serial", "kernel_version", "dtb", "console"):
        if key not in profile:
            raise KeyError(f"profile missing required key: {key}")
    return profile


def resolve_module_file(modules_root: Path, name: str) -> Path | None:
    """Find kernel/<dir>/<name>.ko[.xz] in a module tree."""
    if not modules_root.is_dir():
        return None
    for candidate in sorted(modules_root.rglob(f"{name}.ko")):
        return candidate
    for candidate in sorted(modules_root.rglob(f"{name}.ko.xz")):
        return candidate
    return None


def find_zero3_prepare_block(text: str) -> str:
    """The prepare block that layout.patch_init_script() inserts (fixed mmcblk0p2)."""
    head = "echo 'zero3: prepare image partition and overlay module' > /dev/kmsg"
    start = text.find(head)
    if start == -1:
        raise RuntimeError("zero3 prepare block not found in patched init")
    tail = "fi\n"
    end = text.find(tail, text.find("insmod /usr/lib/modules", start))
    if end == -1:
        raise RuntimeError("zero3 prepare block end not found")
    return text[start : end + len(tail)]


def make_discovery_block(profile: dict, module_version: str, early_modules: dict) -> str:
    board = profile["id"]
    marker = profile["marker"]
    debug_http = bool(profile.get("debug_http", True))
    insmod_lines = "\n".join(
        f"  insmod $mods_dir/{name}.ko >> /tmp/ugos-debug/status.txt 2>&1 || true" for name in early_modules
    )
    http_block = """
/usr/sbin/httpd -p 18080 -h /tmp/ugos-debug >> /tmp/ugos-debug/httpd.log 2>&1 || /usr/bin/busybox httpd -p 18080 -h /tmp/ugos-debug >> /tmp/ugos-debug/httpd.log 2>&1 || true
""" if debug_http else ""
    return f"""echo '{board}: discover marked UGOS image and load early modules' > /dev/kmsg
mkdir -p /tmp/ugos-debug
ugos_stage() {{
  echo "$(date '+%H:%M:%S') $1" >> /image/BOOT-STAGE.txt 2>/dev/null || true
}}
ugos_dump() {{
  cp /tmp/ugos-debug/status.txt /image/STATUS.txt 2>/dev/null || true
  dmesg > /image/DMESG.TXT 2>/dev/null || true
  sync 2>/dev/null || true
}}
echo '{board} initrd debug start' > /tmp/ugos-debug/status.txt
cat /proc/cmdline >> /tmp/ugos-debug/status.txt 2>&1 || true
mods_dir=/usr/lib/modules/{module_version}
{insmod_lines}
ugos_stage 'early modules insmod attempted'
for netif_path in /sys/class/net/*; do
  netif="$(basename "$netif_path")"
  [ "$netif" = "lo" ] && continue
  ip link set "$netif" up >> /tmp/ugos-debug/status.txt 2>&1 || ifconfig "$netif" up >> /tmp/ugos-debug/status.txt 2>&1 || true
  udhcpc -i "$netif" -n -q -t 3 -T 2 -s /bin/true >> /tmp/ugos-debug/status.txt 2>&1 &
done
(
  n=0
  while [ "$n" -lt 120 ]; do
    n=$((n+1))
    {{
      echo '=== UGOS ARM {board} initrd debug ==='
      date 2>/dev/null || true
      echo '--- cmdline ---'
      cat /proc/cmdline 2>/dev/null || true
      echo '--- ip addr ---'
      ip addr 2>/dev/null || ifconfig -a 2>/dev/null || true
      echo '--- mounts ---'
      cat /proc/mounts 2>/dev/null || true
      echo '--- ugos devs ---'
      cat /tmp/ugos-debug/ugos-devs.txt 2>/dev/null || true
      echo '--- target root sanity ---'
      ls -ld /mnt/lib/systemd/systemd /mnt/sbin/init /mnt/ugreen 2>/dev/null || true
      echo '--- image files ---'
      ls -l /image 2>/dev/null || true
    }} > /tmp/ugos-debug/status.txt
    sleep 5
  done
) &{http_block}
mkdir -p /image
UGOS_IMAGE_DEV=''
UGOS_DISK=''
ugos_part() {{
  case "$UGOS_DISK" in
    /dev/mmcblk*) echo "${{UGOS_DISK}}p$1" ;;
    *) echo "${{UGOS_DISK}}$1" ;;
  esac
}}
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
  for cand in /dev/mmcblk[0-9]p2 /dev/mmcblk[0-9][0-9]p2 /dev/sd[a-z]2; do
    [ -e "$cand" ] || continue
    mount -t vfat -o ro "$cand" /image 2>/dev/null || mount -t auto -o ro "$cand" /image 2>/dev/null || continue
    if [ -f /image/rootfs-base.squashfs ] && [ -f /image/{marker} ]; then
      UGOS_IMAGE_DEV="$cand"
      case "$cand" in
        /dev/mmcblk*p2) UGOS_DISK="${{cand%p2}}" ;;
        *) UGOS_DISK="${{cand%2}}" ;;
      esac
      break 2
    fi
    umount /image 2>/dev/null || true
  done
  sleep 1
done
if [ -z "$UGOS_IMAGE_DEV" ]; then
  echo '{board}: marked UGOS image not found; refusing to touch other disks' > /dev/kmsg
  echo 'marked UGOS image not found; halted safely' >> /tmp/ugos-debug/status.txt
  while true; do sleep 60; done
fi
mount -o remount,rw /image 2>/dev/null || true
UGOS_FACTORY_DEV="$(ugos_part 3)"
UGOS_SWAP_DEV="$(ugos_part 5)"
UGOS_UGREEN_DEV="$(ugos_part 6)"
UGOS_OVERLAY_DEV="$(ugos_part 9)"
OVERLAY_DEV="$UGOS_OVERLAY_DEV"
export UGOS_IMAGE_DEV UGOS_FACTORY_DEV UGOS_SWAP_DEV UGOS_UGREEN_DEV UGOS_OVERLAY_DEV OVERLAY_DEV
ugos_stage "marked image found on $UGOS_IMAGE_DEV"
ugos_dump
cat > /tmp/ugos-debug/ugos-devs.txt <<UGOS_DEVS_EOF
UGOS_IMAGE_DEV=$UGOS_IMAGE_DEV
UGOS_FACTORY_DEV=$UGOS_FACTORY_DEV
UGOS_SWAP_DEV=$UGOS_SWAP_DEV
UGOS_UGREEN_DEV=$UGOS_UGREEN_DEV
UGOS_OVERLAY_DEV=$UGOS_OVERLAY_DEV
UGOS_DEVS_EOF
echo "{board}: image=$UGOS_IMAGE_DEV factory=$UGOS_FACTORY_DEV ugreen=$UGOS_UGREEN_DEV overlay=$UGOS_OVERLAY_DEV" > /dev/kmsg
"""


def patch_init_script_generic(layout, text: str, profile: dict, module_version: str, modules_tar: str) -> str:
    # 1. Base zero3-era patch: sgdisk removal, quota mount opts removal, /image prefixing,
    #    seed/register service blocks.  Adds the fixed-mmcblk0p2 prepare block we replace below.
    text = layout.patch_init_script(text, module_version)

    # 2. Replace the fixed prepare block with marked-image discovery (any mmcblk/sd disk).
    old_prepare = find_zero3_prepare_block(text)
    early = profile.get("_early_modules", {})
    new_prepare = make_discovery_block(profile, module_version, early)
    text = text.replace(old_prepare, new_prepare, 1)

    # 3. Q8B lesson: never enable project quota on the overlay device and format
    #    p9 without quota/project features, or first-boot services loop read-only.
    unsafe_tune2fs = """	if ! dumpe2fs -h $OVERLAY_DEV  2>/dev/null | grep -E "Project" > /dev/null; then
		tune2fs -O project $OVERLAY_DEV
	fi
"""
    safe_tune2fs = """	echo 'overlay: project quota enable skipped by base package' > /dev/kmsg
"""
    if unsafe_tune2fs not in text:
        raise RuntimeError("overlay tune2fs project block not found in init")
    text = text.replace(unsafe_tune2fs, safe_tune2fs, 1)
    text = text.replace(
        'mkfs.ext4 -q -L "USER-DATA" -F $OVERLAY_DEV',
        'mkfs.ext4 -q -L "USER-DATA" -F -O ^quota,^project $OVERLAY_DEV',
        1,
    )

    # 4. Board modules + core preinstall extraction into the mounted overlay root.
    core_marker = (
        "\t\tif [ -f /image/core-preinstall.tar.gz ] && [ ! -f /mnt/ugreen/.zero3_core_preinstall_extracted ]; then\n"
        "\t\t\techo \"---zero3 extract core preinstall payload :\" > /dev/kmsg\n"
        "\t\t\ttar -xzf /image/core-preinstall.tar.gz -C /mnt && touch /mnt/ugreen/.zero3_core_preinstall_extracted\n"
        "\t\tfi\n"
    )
    modules_extract = core_marker + (
        f"\t\tif [ -f /image/{modules_tar} ] && [ ! -f /mnt/usr/lib/modules/.ugos_board_modules_extracted ]; then\n"
        f"\t\t\techo \"---{profile['id']} extract board kernel modules :\" > /dev/kmsg\n"
        "\t\t\tmkdir -p /mnt/usr/lib/modules\n"
        f"\t\t\ttar -xzf /image/{modules_tar} -C /mnt && touch /mnt/usr/lib/modules/.ugos_board_modules_extracted\n"
        "\t\tfi\n"
        "\t\tugos_stage 'stage4: payload + modules extracted into overlay root'\n"
        "\t\tugos_dump\n"
    )
    if core_marker not in text:
        raise RuntimeError("core-preinstall extraction block not found in init")
    text = text.replace(core_marker, modules_extract, 1)

    # 4b. Separate marker + sync after the big ugreen.bz2 extraction (freeze forensics).
    unsafe_ugreen = "\t\t\ttar -xf /image/ugreen.bz2 -C /mnt/ugreen && touch /mnt/ugreen/.zero3_ugreen_payload_extracted\n\t\tfi\n"
    safe_ugreen = (
        "\t\t\ttar -xf /image/ugreen.bz2 -C /mnt/ugreen && touch /mnt/ugreen/.zero3_ugreen_payload_extracted\n"
        "\t\tfi\n"
        "\t\tugos_stage 'ugreen payload phase done'\n"
        "\t\tsync 2>/dev/null || true\n"
    )
    if text.count(unsafe_ugreen) != 1:
        raise RuntimeError("ugreen.bz2 extraction block not found exactly once")
    text = text.replace(unsafe_ugreen, safe_ugreen, 1)

    # 5. Identity: replace every zero3 constant with profile values.
    model = profile.get("compatibility_model", DEFAULT_COMPAT_MODEL)
    series = profile.get("model_series", DEFAULT_MODEL_SERIES)
    replacements = [
        (ZERO3_SERIAL, profile["serial"]),
        (ZERO3_HOSTNAME, profile["hostname"]),
        (ZERO3_CPU, profile.get("cpu", {}).get("model", "Generic ARM64")),
        (ZERO3_UUID, profile.get("uuid", ZERO3_UUID)),
        (ZERO3_MAC, profile.get("mac", ZERO3_MAC)),
        ("UGOS-ZERO3", f"UGOS-{profile.get('board_tag', profile['id'].upper())}"),
        (ZERO3_BOARD_NAME, profile["display_name"]),
        ("OPI-ZERO3", profile.get("board_tag", profile["id"].upper())),
        ("DH4300PLUS", model),
        ("dh4300plus", series),
        (ZERO3_BUILD_MARKER, f"ugos-arm-{profile['id']}"),
        ("'/dev/mmcblk0p3'", '"$UGOS_FACTORY_DEV"'),
        ("'/dev/mmcblk0p5'", '"$UGOS_SWAP_DEV"'),
        ("'/dev/mmcblk0p6'", '"$UGOS_UGREEN_DEV"'),
        ('"/dev/mmcblk0p3"', '"$UGOS_FACTORY_DEV"'),
        ('"/dev/mmcblk0p5"', '"$UGOS_SWAP_DEV"'),
        ('"/dev/mmcblk0p6"', '"$UGOS_UGREEN_DEV"'),
        ("/dev/mmcblk0p3", '"$UGOS_FACTORY_DEV"'),
        ("/dev/mmcblk0p5", '"$UGOS_SWAP_DEV"'),
        ("/dev/mmcblk0p6", '"$UGOS_UGREEN_DEV"'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    # 6. Overlay device comes from discovery, never from kernel cmdline parsing.
    unsafe_overlay = "\tOVERLAY_DEV=$(cat /proc/cmdline | awk -F 'overlay=' '{print $2}' | awk -F ' ' '{print $1}')\n"
    safe_overlay = "\tOVERLAY_DEV=\"$UGOS_OVERLAY_DEV\"\n"
    if text.count(unsafe_overlay) != 1:
        raise RuntimeError("command-line overlay device assignment not found exactly once")
    text = text.replace(unsafe_overlay, safe_overlay, 1)

    # 7. Non-UGREEN boards have no MCU (line was already chroot-wrapped by the base patch).
    text = text.replace(
        "chroot /mnt /usr/sbin/mcu_ota_upgrader || echo 'zero3: mcu upgrader skipped' > /dev/kmsg",
        f"echo '{profile['id']}: no UGREEN MCU; mcu_ota_upgrader disabled' > /dev/kmsg",
        1,
    )

    # 8. Root switch: explicit sanity check + chroot-based switch.  On A5E the busybox
    #    switch_root printed its usage error (its NEW_INIT sanity check failed) even
    #    though OECT booted the identical line -- so v5 stops guessing and checks
    #    /mnt/lib/systemd/systemd directly, dumps state, then switches via chroot.
    unsafe_exec = '\techo "---zero3 exec switch_root /mnt /lib/systemd/systemd" > /dev/kmsg\n\texec switch_root /mnt /lib/systemd/systemd\n'
    safe_exec = (
        '\techo "---zero3 exec switch_root /mnt /lib/systemd/systemd" > /dev/kmsg\n'
        "\tugos_stage 'stage5: pre-switch sanity check'\n"
        "\tls -ld /mnt/lib /mnt/lib/systemd/systemd /mnt/sbin/init /mnt/usr /mnt/ugreen >> /tmp/ugos-debug/status.txt 2>&1 || true\n"
        "\tugos_dump\n"
        "\tif [ -x /mnt/lib/systemd/systemd ]; then\n"
        f"\t\techo '{profile['id']}: systemd present in assembled root; switching via chroot' > /dev/kmsg\n"
        "\t\tcd /mnt\n"
        "\t\texec chroot . /lib/systemd/systemd\n"
        "\tfi\n"
        f"\techo '{profile['id']}: systemd missing in assembled root; dumping state' > /dev/kmsg\n"
        "\tugos_dump\n"
        "\texec switch_root /mnt /lib/systemd/systemd\n"
    )
    if text.count(unsafe_exec) != 1:
        raise RuntimeError("stage5 exec block not found exactly once")
    text = text.replace(unsafe_exec, safe_exec, 1)
    # 8b. Mock-cloud bridge (v11): point the board's UGREEN cloud API domains at the
    #     self-hosted server and trust its CA, so app_serv's catalog/banner/OTA calls
    #     hit our mock endpoints instead of failing 401.
    mock = profile.get("mock_cloud") or {}
    if mock.get("server_ip") and mock.get("ca_cert"):
        ca_src = Path(mock["ca_cert"])
        if not ca_src.is_absolute():
            ca_src = Path(__file__).resolve().parents[2] / ca_src
        ca_pem = ca_src.read_text(encoding="utf-8").strip()
        domains = " ".join(mock.get("domains", []))
        block = (
            "\t\tmkdir -p /mnt/usr/local/share/ca-certificates\n"
            "\t\tcat > /mnt/usr/local/share/ca-certificates/opugos-mock-ca.crt <<'UGOS_CA_EOF'\n"
            f"{ca_pem}\n"
            "UGOS_CA_EOF\n"
            "\t\tchroot /mnt /usr/sbin/update-ca-certificates >> /tmp/ugos-debug/status.txt 2>&1 || true\n"
            "\t\tfor dom in " + domains + '; do grep -q " $dom" /mnt/etc/hosts 2>/dev/null || echo "' + mock["server_ip"] + ' $dom" >> /mnt/etc/hosts; done\n'
            "\t\tugos_stage 'mock-cloud bridge installed (hosts + CA)'\n"
        )
        anchor = "\t\tugos_stage 'stage4: payload + modules extracted into overlay root'\n\t\tugos_dump\n"
        if anchor not in text:
            raise RuntimeError("stage4 anchor not found for mock-cloud injection")
        text = text.replace(anchor, anchor + block, 1)
    return text


def build_initrd(layout, payload_dir: Path, device_dir: Path, profile: dict, out_path: Path) -> dict:
    initfs = payload_dir / "initfs.tar.gz"
    require_file(initfs, "UGOS initfs.tar.gz")
    module_version = profile["kernel_version"]
    modules_root = device_dir / "rootfs-overlay" / "usr" / "lib" / "modules" / module_version
    require_dir(modules_root, "board module tree")

    early_modules = {}
    for name in profile.get("initramfs_modules", []):
        found = resolve_module_file(modules_root, name)
        if found is None:
            raise FileNotFoundError(f"module {name!r} not found under {modules_root}")
        early_modules[name] = found
    profile["_early_modules"] = early_modules

    writer = layout.NewcWriter()
    counts = {"dir": 0, "sym": 0, "hardlink": 0, "file": 0}
    patched_init = False

    with tarfile.open(initfs, "r:gz") as tar:
        for member in tar.getmembers():
            name = layout.normalize_tar_name(member.name)
            if not name:
                continue
            mtime = int(member.mtime or 0)
            if member.isdir():
                writer.add(name, 0o040000 | (member.mode & 0o777), b"", nlink=2, mtime=mtime)
                counts["dir"] += 1
            elif member.issym():
                writer.add(name, 0o120000 | 0o777, member.linkname.encode("utf-8"), mtime=mtime)
                counts["sym"] += 1
            elif member.islnk():
                target = layout.normalize_tar_name(member.linkname)
                writer.add(name, 0o120000 | 0o777, f"/{target}".encode("utf-8"), mtime=mtime)
                counts["hardlink"] += 1
            elif member.isfile():
                extracted = tar.extractfile(member)
                data = extracted.read() if extracted is not None else b""
                if name == "usr/sbin/init":
                    data = patch_init_script_generic(
                        layout, data.decode("utf-8", errors="replace"), profile, module_version,
                        modules_tar=f"{profile['id']}-modules.tar.gz",
                    ).encode("utf-8")
                    patched_init = True
                writer.add(name, 0o100000 | (member.mode & 0o777), data, mtime=mtime)
                counts["file"] += 1

    now = int(time.time())
    module_dirs = ["usr/lib/modules", f"usr/lib/modules/{module_version}"]
    for name in module_dirs:
        writer.add(name, 0o040755, b"", nlink=2, mtime=now)
    for name, source in early_modules.items():
        # flat under <ver>/ to match the discovery block's insmod $mods_dir/<name>.ko lines;
        # always stored decompressed: busybox insmod in the initramfs cannot load .ko.xz
        data = lzma.decompress(source.read_bytes()) if source.name.endswith(".xz") else source.read_bytes()
        writer.add(f"usr/lib/modules/{module_version}/{name}.ko", 0o100644, data, mtime=now)
    writer.add("init", 0o100755, b"#!/bin/sh\nexec /usr/sbin/init \"$@\"\n", mtime=now)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw = writer.finish()
    out_path.write_bytes(gzip.compress(raw, compresslevel=6, mtime=0))
    return {
        "initrd": str(out_path),
        "initrd_bytes": out_path.stat().st_size,
        "raw_cpio_bytes": len(raw),
        "patched_init": patched_init,
        "counts": counts,
        "early_modules": {n: str(p) for n, p in early_modules.items()},
    }


def make_boot_tree(base, device_dir: Path, profile: dict, initrd: Path):
    bootfs = device_dir / "bootfs"
    image = bootfs / "Image"
    dtb = bootfs / profile["dtb"]
    require_file(image, "board kernel Image")
    require_file(dtb, f"board DTB {profile['dtb']}")
    module_version = profile["kernel_version"]
    console = profile["console"]
    console_secondary = profile.get("console_secondary", "")
    earlycon = profile.get("earlycon", "")
    extra = profile.get("bootargs_extra", "")
    bootargs = (
        f"console={console} {console_secondary} root=/dev/ram0 rootwait overlayfs=ext4 loglevel=7 "
        f"net.ifnames=0 biosdevname=0 panic=10 consoleblank=0 {earlycon} {extra}"
    ).strip()
    extlinux = f"""TIMEOUT 10
DEFAULT UGOS-{profile['board_tag']}

LABEL UGOS-{profile['board_tag']}
  MENU LABEL UGOS Pro for {profile['display_name']}
  LINUX /Image
  INITRD /initrd.gz
  FDT /{profile['dtb']}
  APPEND {bootargs}
"""
    boot_cmd = f"""if test -z "${{distro_bootpart}}"; then setenv distro_bootpart 1; fi
setenv ugos_dtb /{profile['dtb']}
setenv ugos_kernel /Image
setenv ugos_initrd /initrd.gz
setenv bootargs {bootargs}
echo Loading UGOS Pro {profile['display_name']} boot script
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{ramdisk_addr_r}} ${{ugos_initrd}}
setenv ugos_initrd_size ${{filesize}}
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{kernel_addr_r}} ${{ugos_kernel}}
load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{fdt_addr_r}} ${{ugos_dtb}}
fdt addr ${{fdt_addr_r}}
fdt resize 65536
if test -n "${{pxefile_addr_r}}"; then
  if load ${{devtype}} ${{devnum}}:${{distro_bootpart}} ${{pxefile_addr_r}} marker-src.txt; then
    if fatwrite ${{devtype}} ${{devnum}}:1 ${{pxefile_addr_r}} UBOOTOK.TXT ${{filesize}}; then
      echo wrote UBOOTOK.TXT stage marker
    fi
  fi
fi
booti ${{kernel_addr_r}} ${{ramdisk_addr_r}}:${{ugos_initrd_size}} ${{fdt_addr_r}}
"""
    armbian_env = f"""verbosity=7
console=serial
bootlogo=false
fdtfile={profile['dtb']}
rootdev=/dev/ram0
rootfstype=ext4
extraargs={bootargs}
"""
    readme = f"""UGOS Pro base package image for {profile['display_name']}

Serial: {profile['serial']}
Hostname: {profile['hostname']}
Kernel: {module_version}
Console: {console}
Marker partition: p2 must contain rootfs-base.squashfs + {profile['marker']}
"""
    root = base.FatNode("", True)
    base.add_file(root, "Image", source=image)
    base.add_file(root, "initrd.gz", source=initrd)
    base.add_file(root, profile["dtb"], source=dtb)
    base.add_file(root, "armbianEnv.txt", data=armbian_env.encode("ascii", errors="replace"))
    base.add_file(root, "extlinux/extlinux.conf", data=extlinux.encode("ascii", errors="replace"))
    base.add_file(root, "boot/extlinux/extlinux.conf", data=extlinux.encode("ascii", errors="replace"))
    boot_scr = base.make_uboot_script_image(boot_cmd, name=f"UGOS-{profile['board_tag']}")
    base.add_file(root, "boot.cmd", data=boot_cmd.encode("ascii", errors="replace"))
    base.add_file(root, "boot.scr", data=boot_scr)
    base.add_file(root, "boot.scr.uimg", data=boot_scr)
    base.add_file(root, "marker-src.txt", data=b"u-boot-stage-ok\n")
    base.add_file(root, "README-UGOS.txt", data=readme.encode("ascii", errors="replace"))
    return root


def ensure_modules_tar(device_dir: Path, profile: dict) -> Path:
    module_version = profile["kernel_version"]
    modules_root = device_dir / "rootfs-overlay" / "usr" / "lib" / "modules" / module_version
    require_file(modules_root / "modules.dep", "modules.dep in board module tree")  # file check is intentional
    out = device_dir / f"{profile['id']}-modules.tar.gz"
    if out.is_file():
        return out
    with tarfile.open(out, "w:gz") as tar:
        tar.add(modules_root.parent, arcname="usr/lib/modules")
    return out


def make_image_tree(base, payload_dir: Path, core_preinstall: Path, device_dir: Path, profile: dict, modules_tar: Path):
    payload = payload_dir
    preinstall = core_preinstall
    names = [
        "rootfs-base.squashfs",
        "kernel.squashfs",
        "apt.squashfs",
        "fw.squashfs",
        "oem.squashfs",
        "ugreen.bz2",
    ]
    root = base.FatNode("", True)
    files = []
    for name in names:
        path = payload / name
        require_file(path, f"UGOS {name}")
        base.add_file(root, name, source=path)
        files.append(name)
    require_file(preinstall, "UGOS core preinstall tarball")
    base.add_file(root, "core-preinstall.tar.gz", source=preinstall)
    files.append("core-preinstall.tar.gz")
    base.add_file(root, modules_tar.name, source=modules_tar)
    files.append(modules_tar.name)
    marker_data = f"UGOS Pro base package image for {profile['display_name']} ({profile['marker']})\n".encode("utf-8")
    base.add_file(root, profile["marker"], data=marker_data)
    files.append(profile["marker"])
    base.add_file(
        root,
        "README-UGOS-IMAGES.txt",
        data=b"UGOS payloads, core preinstall, and board modules for the marked-image initramfs.\n",
    )
    return root, files


def zero_range(path: Path, offset: int, length: int, chunk_size: int = 1024 * 1024) -> None:
    zeros = b"\x00" * min(chunk_size, length)
    remaining = length
    with path.open("r+b") as f:
        f.seek(offset)
        while remaining:
            size = min(len(zeros), remaining)
            f.write(zeros[:size])
            remaining -= size


def check_bootloader_magics(out_image: Path, profile: dict) -> dict:
    results = {}
    with out_image.open("rb") as f:
        for check in profile.get("bootloader", {}).get("magic_checks", []):
            f.seek(check["offset"])
            data = f.read(len(check["bytes"]) // 2)
            expect = bytes.fromhex(check["bytes"])
            results[check.get("label", hex(check["offset"]))] = data == expect
    return results


def main():
    parser = argparse.ArgumentParser(description="Build a UGOS Pro ARM64 image from a device profile.")
    parser.add_argument("--profile", required=True, help="Path to profiles/<id>/profile.json")
    parser.add_argument("--payload-dir", default=r"H:/ugos/payload", help="UGOS ARM payload dir (squashfs/initfs/ugreen.bz2)")
    parser.add_argument(
        "--core-preinstall",
        default=r"H:/ugos/core-preinstall/core-preinstall.tar.gz",
        help="core-preinstall tarball path",
    )
    parser.add_argument(
        "--out-image",
        default=None,
        help="Canonical output (overwrite semantics): out/ugos-arm64-<id>.img. Do NOT add version suffixes.",
    )
    parser.add_argument("--disk-signature", default=None)
    parser.add_argument("--keep-work", action="store_true", help="Keep intermediate work files (debug only)")
    args = parser.parse_args()

    profile_path = Path(args.profile).resolve()
    profile = load_profile(profile_path)
    repo_root = Path(__file__).resolve().parents[2]
    device_dir_raw = profile.get("device_dir") or f"boards/{profile['id']}-base"
    device_dir = Path(device_dir_raw)
    if not device_dir.is_absolute():
        device_dir = (repo_root / device_dir).resolve()
    require_dir(device_dir, f"device dir for {profile['id']}")
    payload_dir = Path(args.payload_dir).resolve()
    core_preinstall = Path(args.core_preinstall).resolve()

    if args.out_image:
        out_image = Path(args.out_image).resolve()
    else:
        out_image = Path(__file__).resolve().parents[1] / "out" / f"ugos-arm64-{profile['id']}.img"

    scripts_dir = Path(__file__).resolve().parent
    layout = load_module(scripts_dir / "build-layout-debug-image.py", "ugos_layout_builder")
    base = layout.load_base_builder(scripts_dir.parent)

    work_dir = out_image.parent / "work" / profile["id"]
    work_dir.mkdir(parents=True, exist_ok=True)
    boot_part = work_dir / "boot-fat32.img"
    image_part = work_dir / "ugos-images-fat32.img"
    initrd = work_dir / "initrd.gz"
    manifest_path = out_image.with_suffix(out_image.suffix + ".manifest.json")
    sha_path = out_image.with_suffix(out_image.suffix + ".sha256")

    # core-preinstall is device-independent; rebuild only when missing.
    preinstall_tar = core_preinstall
    if not preinstall_tar.is_file():
        raise FileNotFoundError(f"missing core-preinstall tarball: {preinstall_tar}")

    initrd_info = build_initrd(layout, payload_dir, device_dir, profile, initrd)
    primary, logicals, image_size = layout.layout_partitions()
    if primary[0]["start_lba"] != 32768:
        raise RuntimeError("bootloader blob layout expects p1 to start at LBA 32768 (16 MiB)")

    blob_path = device_dir / profile.get("bootloader", {}).get("image", "bootloader-region-16m.bin")
    require_file(blob_path, "board bootloader blob")
    blob_bytes = blob_path.stat().st_size
    if blob_bytes > primary[0]["start_lba"] * SECTOR_SIZE:
        raise RuntimeError("bootloader blob larger than reserved pre-partition region")
    disk_signature = int(args.disk_signature, 16) if args.disk_signature else int(profile.get("disk_signature", "0x55414733"), 16)

    modules_tar = ensure_modules_tar(device_dir, profile)
    boot_tree = make_boot_tree(base, device_dir, profile, initrd)
    image_tree, image_files = make_image_tree(base, payload_dir, core_preinstall, device_dir, profile, modules_tar)
    base.build_fat32_image(boot_part, boot_tree, primary[0]["sectors"], primary[0]["start_lba"], disk_signature)
    base.build_fat32_image(image_part, image_tree, primary[1]["sectors"], primary[1]["start_lba"], disk_signature ^ 0x2222)

    out_image.parent.mkdir(parents=True, exist_ok=True)
    with out_image.open("wb") as f:
        f.truncate(image_size)
    layout.copy_into(blob_path, out_image, 0)
    # kill stale partition metadata in LBA 1..63 (GPT header + entries) while keeping
    # everything the SoC boot ROM needs that lives higher in the reserved region
    zero_range(out_image, SECTOR_SIZE, 63 * SECTOR_SIZE)
    partitions = layout.write_mbr_and_ebr(out_image, disk_signature, primary, logicals)
    layout.copy_into(boot_part, out_image, primary[0]["start_lba"] * SECTOR_SIZE)
    layout.copy_into(image_part, out_image, primary[1]["start_lba"] * SECTOR_SIZE)

    with out_image.open("rb") as vf:
        mbr = vf.read(SECTOR_SIZE)
        vf.seek(SECTOR_SIZE)
        stale = vf.read(63 * SECTOR_SIZE)
        vf.seek(131072)
        boot0_head = vf.read(16)
    digest = base.sha256_file(out_image)
    sha_path.write_text(f"{digest}  {out_image.name}\n", encoding="ascii")
    manifest = {
        "board": profile["id"],
        "board_name": profile["display_name"],
        "profile": str(profile_path),
        "device_dir": str(device_dir),
        "image": str(out_image),
        "image_bytes": image_size,
        "sha256": digest,
        "disk_signature": f"0x{disk_signature:08x}",
        "hostname": profile["hostname"],
        "serial": profile["serial"],
        "compatibility_model": profile.get("compatibility_model", DEFAULT_COMPAT_MODEL),
        "cpu_model": profile.get("cpu", {}).get("model"),
        "kernel_version": profile["kernel_version"],
        "dtb": profile["dtb"],
        "console": profile["console"],
        "bootloader_blob": str(blob_path),
        "bootloader_blob_bytes": blob_bytes,
        "marker": profile["marker"],
        "cmdline_bootargs_extra": profile.get("bootargs_extra", ""),
        "initrd": initrd_info,
        "partitions": partitions,
        "ugos_image_partition_files": image_files,
        "verification": {
            "mbr_signature_ok": mbr[510:512] == b"\x55\xAA",
            "sectors_1_to_63_zeroed": all(b == 0 for b in stale),
            "boot0_magic_offset_128k": boot0_head[4:12] == bytes.fromhex("65474f4e2e425430"),
            "bootloader_magic_checks": check_bootloader_magics(out_image, profile),
        },
        "notes": [
            "Generic base-package build: identity, modules, DTB, bootloader and marker all come from the device profile.",
            "initramfs accepts only a p2 containing rootfs-base.squashfs plus the marker file; otherwise it halts without touching other disks.",
            "Overlay p9 is formatted without quota/project and the tune2fs project-enable path is disabled (Q8B lesson).",
            "Board modules tar is extracted into the overlay RW layer, shadowing the RK3588 kernel.squashfs modules.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if not args.keep_work:
        # canonical builds keep only the image + manifest + sha; intermediates are
        # regenerable and writing them over and over just wears the SSD
        import shutil as _shutil
        _shutil.rmtree(work_dir, ignore_errors=True)

    print(f"Wrote image: {out_image}")
    print(f"Wrote manifest: {manifest_path}")
    print(f"Wrote sha256: {sha_path}")
    print(f"Image size: {image_size} bytes")
    print(f"SHA256: {digest}")
    print(f"Verification: {manifest['verification']}")
    ok = all(manifest["verification"].values()) if manifest["verification"]["bootloader_magic_checks"] else None
    if ok is False:
        raise SystemExit("verification failed -- see manifest")


if __name__ == "__main__":
    main()
