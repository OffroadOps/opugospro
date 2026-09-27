"""Server-side v12 build: upload base scripts + profiles + CA, assemble inputs, run builder, 7z output."""
import os
import stat
import time

import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"
BASE = r"H:\ugos\base"

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()


def run(cmd, timeout=3000):
    _o, out, err = cli.exec_command(cmd, timeout=timeout)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    print(f"$ {cmd[:90]}\n{o.strip()[:1500]}{('[err] ' + e.strip()[:500]) if e.strip() else ''}\n", flush=True)
    return o


def sftp_mkdir(path):
    cur = ""
    for part in path.strip("/").split("/"):
        cur += "/" + part
        try:
            sftp.stat(cur)
        except FileNotFoundError:
            sftp.mkdir(cur)


def put(local, remote):
    sftp_mkdir(os.path.dirname(remote))
    sftp.put(local, remote)
    print(f"put {remote}")


run("mkdir -p /srv/ugos/opugospro/base/profiles/radxa-cubie-a5e /srv/ugos/opugospro/boards/radxa-cubie-a5e-base/opugos-mock-ca.crt.d /srv/ugos/build-inputs /srv/ugos-mixproj")
run("rm -f /srv/ugos/build-inputs/payload.tar.gz")

# build inputs: mixed payload archive with payload/ prefix
run("mkdir -p /srv/ugos/payload-mix/payload && mv /srv/ugos/payload-mix/*.squashfs /srv/ugos/payload-mix/*.tar.gz /srv/ugos/payload-mix/*.bz2 /srv/ugos/payload-mix/payload/ 2>/dev/null; cd /srv/ugos/payload-mix && tar czf /srv/ugos/build-inputs/payload.tar.gz payload && ls -la /srv/ugos/build-inputs/payload.tar.gz", timeout=1200)

# core-preinstall: rebuild from the 1.20 ugreen.bz2
put(r"H:\ugos\base\scripts\build-core-preinstall.py", "/srv/ugos/opugospro/base/scripts/build-core-preinstall.py")
run("mkdir -p /srv/ugos-mixproj/payload && ln -sfn /srv/ugos/payload-mix/payload/ugreen.bz2 /srv/ugos-mixproj/payload/ugreen.bz2 2>/dev/null; ln -sfn /srv/ugos/payload-mix/payload /srv/ugos-mixproj/payload 2>/dev/null; ls -la /srv/ugos-mixproj/payload/ | head -3")
run("cd /srv/ugos/opugospro && python3 base/scripts/build-core-preinstall.py --project-dir /srv/ugos-mixproj --out /srv/ugos/build-inputs/core-preinstall.tar.gz", timeout=1800)

# base scripts + profiles + board CA
for f in ["build-ugos-arm-image.py", "build-layout-debug-image.py", "build-squashfs-debug-image.py"]:
    put(os.path.join(BASE, "scripts", f), f"/srv/ugos/opugospro/base/scripts/{f}")
put(os.path.join(BASE, "profiles", "radxa-cubie-a5e", "profile.json"), "/srv/ugos/opugospro/base/profiles/radxa-cubie-a5e/profile.json")
put(r"H:\ugos\boards\radxa-cubie-a5e-base\opugos-mock-ca.crt", "/srv/ugos/opugospro/boards/radxa-cubie-a5e-base/opugos-mock-ca.crt")

# board assets on the VPS: assemble board dir from the build-input board tar
run("cd /srv/ugos/opugospro && tar xzf /srv/ugos/build-inputs/board-radxa-cubie-a5e.tar.gz && ls boards/radxa-cubie-a5e-base/ | head -6", timeout=600)

# fix profile ca_cert path for the VPS layout (already relative) + run the build
run("cd /srv/ugos/opugospro && python3 base/scripts/build-ugos-arm-image.py --profile base/profiles/radxa-cubie-a5e/profile.json --payload-dir /srv/ugos/payload-mix/payload --core-preinstall /srv/ugos/build-inputs/core-preinstall.tar.gz", timeout=3000)

# compress output
run("cd /srv/ugos/opugospro/base/out && 7z a -mx3 opugospro-a5e.7z *.img 2>&1 | tail -2 && ls -la /srv/ugos/opugospro/base/out/", timeout=1800)
run("mv /srv/ugos/opugospro/base/out/opugospro-a5e.7z /srv/ugos/updates/opugospro-a5e-1.20.0.0142-$(date +%Y%m%d).7z && ls -la /srv/ugos/updates/")
cli.close()
print("V12 SERVER-SIDE BUILD DONE")
