import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

cmds = [
    "mkdir -p /srv/ugos/payload-1.20 && cd /srv/ugos/official-fw && tar xf *.img -C /srv/ugos/payload-1.20 ./fw.squashfs ./oem.squashfs ./kernel.squashfs ./initfs.tar.gz ./ugreen.bz2 ./os-release ./ugreen-os-release.json && ls -la /srv/ugos/payload-1.20/",
    # extract new initfs init for anchor comparison
    "mkdir -p /tmp/initfs120 && cd /tmp/initfs120 && tar xzf /srv/ugos/payload-1.20/initfs.tar.gz ./usr/sbin/init 2>&1 | head -2; ls -la usr/sbin/init 2>/dev/null",
    # check new ugreen.bz2 @cache UPK list
    "python3 - <<'EOF'\nimport tarfile\nt = tarfile.open('/srv/ugos/payload-1.20/ugreen.bz2', 'r:*')\nnames = [n for n in t.getnames() if n.endswith('.upk')]\nprint('UPKs in 1.20 payload:', len(names))\nfor n in sorted(names): print(' ', n)\nEOF",
]
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
for c in cmds:
    _o, out, err = cli.exec_command(c, timeout=900)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    print(f"$ {c[:80]}\n{o.strip()[:1800]}{('[err] ' + e.strip()[:300]) if e.strip() else ''}\n{'='*50}")
cli.close()
