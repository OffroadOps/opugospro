#!/usr/bin/env sh
set -eu

DEFAULT_CONFHOME="http://5.181.177.120/ugos-installer"
DEFAULT_IMG_URL="http://5.181.177.120/ugospro-1.19.1.126-amd64-universal-bios-uefi-gpt-dd.img.zst"

CONFHOME=${UGOS_CONFHOME:-$DEFAULT_CONFHOME}
IMG_URL=${UGOS_IMG_URL:-$DEFAULT_IMG_URL}
TARGET_DISK=${UGOS_TARGET_DISK:-}
FORCE_BOOT_MODE=${UGOS_FORCE_BOOT_MODE:-}
HOLD=${UGOS_HOLD:-}
REINSTALL_PASSWORD=${UGOS_REINSTALL_PASSWORD:-}

usage() {
    cat <<EOF
Usage:
  sh ugos-install.sh [options]

Options:
  --img URL                 UGOS DD image URL.
  --confhome URL            URL directory containing patched reinstall.sh/trans.sh.
  --target-disk DEV         Target disk, for example /dev/vda or /dev/sda.
  --force-boot-mode MODE    bios or efi.
  --hold N                  Pass --hold to reinstall.sh. Values: 0, 1, 2.
  --password PASSWORD       Temporary password for the reinstall live environment.
  -h, --help                Show help.

Environment overrides:
  UGOS_IMG_URL
  UGOS_CONFHOME
  UGOS_TARGET_DISK
  UGOS_FORCE_BOOT_MODE
  UGOS_HOLD
  UGOS_REINSTALL_PASSWORD
EOF
}

die() {
    echo "ERROR: $*" >&2
    exit 1
}

need_root() {
    [ "$(id -u)" = 0 ] || die "Please run as root."
}

download() {
    url=$1
    out=$2
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$url" -o "$out"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$out" "$url"
    else
        die "curl or wget is required."
    fi
}

random_password() {
    if command -v openssl >/dev/null 2>&1; then
        openssl rand -base64 18 | tr -d '=+/' | cut -c1-16
    elif [ -r /dev/urandom ]; then
        tr -dc 'A-Za-z0-9' </dev/urandom | head -c 16
        echo
    else
        echo "ugos$(date +%s)$$"
    fi
}

while [ "$#" -gt 0 ]; do
    case "$1" in
    --img)
        [ "$#" -ge 2 ] || die "Need value for --img."
        IMG_URL=$2
        shift 2
        ;;
    --confhome)
        [ "$#" -ge 2 ] || die "Need value for --confhome."
        CONFHOME=$2
        shift 2
        ;;
    --target-disk)
        [ "$#" -ge 2 ] || die "Need value for --target-disk."
        TARGET_DISK=$2
        shift 2
        ;;
    --force-boot-mode)
        [ "$#" -ge 2 ] || die "Need value for --force-boot-mode."
        FORCE_BOOT_MODE=$2
        shift 2
        ;;
    --hold)
        [ "$#" -ge 2 ] || die "Need value for --hold."
        HOLD=$2
        shift 2
        ;;
    --password)
        [ "$#" -ge 2 ] || die "Need value for --password."
        REINSTALL_PASSWORD=$2
        shift 2
        ;;
    -h | --help)
        usage
        exit 0
        ;;
    *)
        die "Unknown option: $1"
        ;;
    esac
done

case "$FORCE_BOOT_MODE" in
"" | bios | efi) ;;
*) die "--force-boot-mode must be bios or efi." ;;
esac

case "$HOLD" in
"" | 0 | 1 | 2) ;;
*) die "--hold must be 0, 1, or 2." ;;
esac

need_root

CONFHOME=${CONFHOME%/}
tmp_dir=${TMPDIR:-/tmp}/ugos-installer.$$
mkdir -p "$tmp_dir"
trap 'rm -rf "$tmp_dir"' EXIT

if [ -z "$REINSTALL_PASSWORD" ]; then
    REINSTALL_PASSWORD=$(random_password)
fi

reinstall_sh=$tmp_dir/reinstall.sh
download "$CONFHOME/reinstall.sh" "$reinstall_sh"
chmod +x "$reinstall_sh"

echo "UGOS installer"
echo "  confhome: $CONFHOME"
echo "  image:    $IMG_URL"
if [ -n "$TARGET_DISK" ]; then
    echo "  disk:     $TARGET_DISK"
else
    echo "  disk:     auto"
fi
echo "  live SSH user:     root"
echo "  live SSH password: $REINSTALL_PASSWORD"
echo
echo "The password above is only for the temporary reinstall live environment."
echo "It will not become the UGOS administrator password."
echo

export UGOS_CONFHOME=$CONFHOME

set -- dd --img "$IMG_URL" --ugos --user root --password "$REINSTALL_PASSWORD"

if [ -n "$TARGET_DISK" ]; then
    set -- "$@" --target-disk "$TARGET_DISK"
fi
if [ -n "$FORCE_BOOT_MODE" ]; then
    set -- "$@" --force-boot-mode "$FORCE_BOOT_MODE"
fi
if [ -n "$HOLD" ]; then
    set -- "$@" --hold "$HOLD"
fi

exec sh "$reinstall_sh" "$@"
