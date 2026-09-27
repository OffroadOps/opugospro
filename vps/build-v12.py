import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

cmds = [
    # assemble mixed payload: 1.17 rootfs/apt + 1.20 fw/oem/kernel/initfs/ugreen
    "mkdir -p /srv/ugos/payload-mix && cd /srv/ugos/build-inputs && tar xzf payload.tar.gz payload/rootfs-base.squashfs payload/apt.squashfs 2>&1 | head -2; cp payload/rootfs-base.squashfs payload/apt.squashfs /srv/ugos/payload-mix/ && cp /srv/ugos/payload-1.20/{fw.squashfs,oem.squashfs,kernel.squashfs,initfs.tar.gz,ugreen.bz2} /srv/ugos/payload-mix/ && ls -la /srv/ugos/payload-mix/",
    # repack build input archive (new mixed payload)
    "cd /srv/ugos/payload-mix && tar czf /srv/ugos/build-inputs/payload.tar.gz payload 2>&1 | head -2; ls -la /srv/ugos/build-inputs/payload.tar.gz",
]
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
for c in cmds:
    _o, out, err = cli.exec_command(c, timeout=1800)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    print(f"$ {c[:80]}\n{o.strip()[:1200]}{('[err] ' + e.strip()[:400]) if e.strip() else ''}\n{'='*50}")
cli.close()
