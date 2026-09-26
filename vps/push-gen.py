import os
import sys
"""Upload catalog generator + signing key to VPS, install deps, run it."""
import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()


def run(cmd, timeout=600):
    _o, out, err = cli.exec_command(cmd, timeout=timeout)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    print(f"$ {cmd[:70]}\n{o.strip()[:1500]}{('[stderr] ' + e.strip()[:400]) if e.strip() else ''}\n")
    return o


run("mkdir -p /etc/ugos-store /srv/ugos-tools && which python3 || apt-get install -y -qq python3 2>&1 | tail -1")
run("python3 -c 'import cryptography' 2>/dev/null || (apt-get update -qq && apt-get install -y -qq python3-cryptography 2>&1 | tail -1)")
sftp.put(r"H:\ugos\vps\gen-catalog.py", "/srv/ugos-tools/gen-catalog.py")
sftp.put(r"H:\ugos\x86\ugos-community-store\private\signing-key.pem", "/etc/ugos-store/signing-key.pem")
run("chmod 600 /etc/ugos-store/signing-key.pem")
run("python3 /srv/ugos-tools/gen-catalog.py", timeout=1800)
run("mkdir -p /www/store && cp /www/store/repo.json /www/store/repo.json 2>/dev/null; ls -la /www/store/ && curl -s https://ugospro.135246.xyz/store/repo.json | head -c 200; echo")
cli.close()
