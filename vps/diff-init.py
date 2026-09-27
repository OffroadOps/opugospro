import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

script = r'''
python3 - <<'EOF'
import tarfile, hashlib

def init_sha_and_text(tarpath, member='./usr/sbin/init'):
    t = tarfile.open(tarpath, 'r:gz')
    m = t.getmember(member)
    data = t.extractfile(m).read()
    return hashlib.sha256(data).hexdigest()[:16], len(data), data.decode('utf-8', errors='replace')

h1, l1, t1 = init_sha_and_text('/srv/ugos/payload-1.20/initfs.tar.gz')
print('1.20 init:', h1, l1, 'bytes')
# anchors used by our patch chain
anchors = [
    "PART_ERR=`sgdisk",
    "mount -t $OVERLAY_FS -o rw,nosuid,nodev,noatime,nobarrier,quota",
    "mount -t tmpfs tmpfs /tmp",
    "zero3: prepare image partition and overlay module",
    "if [ -f /image/core-preinstall.tar.gz ]",
    "---go move proc :",
    "exec switch_root /mnt /lib/systemd/systemd",
    "pivot_root /mnt /mnt/rootfs",
    "OVERLAY_DEV=$(cat /proc/cmdline",
    "mkfs.ext4 -q -L",
    "/usr/sbin/mcu_ota_upgrader",
    "chroot /mnt /usr/sbin/mcu_ota_upgrader",
]
for a in anchors:
    print(f'  [{"OK " if a in t1 else "MISS"}] {a[:70]}')
# storage of the file for further diff
open('/srv/ugos-tools/init-120.txt','w').write(t1)
EOF
'''
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
_o, out, err = cli.exec_command(script, timeout=120)
print(out.read().decode("utf-8", errors="replace"))
print(err.read().decode()[-300:])
cli.close()
