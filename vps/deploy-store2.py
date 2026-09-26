"""Robust store deployment: single-archive upload with retries, then remote extract + nginx + certbot."""
import io
import os
import subprocess
import sys
import tarfile
import time

import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD
PUBLIC = r"H:\ugos\x86\ugos-community-store\public"
ARCHIVE_LOCAL = r"H:\ugos\vps\store-public.tar.gz"


def make_archive():
    files = []
    with tarfile.open(ARCHIVE_LOCAL, "w:gz") as tar:
        for root, _dirs, fs in os.walk(PUBLIC):
            for f in fs:
                full = os.path.join(root, f)
                arc = os.path.relpath(full, PUBLIC).replace("\\", "/")
                tar.add(full, arcname=arc)
                if os.path.getsize(full) > 4 * 1024 * 1024:
                    files.append(f)
    print(f"archive: {os.path.getsize(ARCHIVE_LOCAL):,} bytes, {len(files)} big files")


def connect():
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
    return cli


def run(cli, cmd, timeout=600):
    _o, out, err = cli.exec_command(cmd, timeout=timeout)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    code = out.channel.recv_exit_status()
    return code, o.strip(), e.strip()


def upload_with_retry(cli, attempts=5):
    sftp = cli.open_sftp()
    remote = "/srv/ugos/store-public.tar.gz"
    local_size = os.path.getsize(ARCHIVE_LOCAL)
    for i in range(1, attempts + 1):
        try:
            print(f"upload attempt {i} ({local_size:,} bytes)...")
            t0 = time.time()
            sftp.put(ARCHIVE_LOCAL, remote)
            _c, o, _e = run(cli, f"stat -c %s {remote}")
            if o.strip() == str(local_size):
                print(f"uploaded OK in {time.time()-t0:.0f}s")
                return True
            print(f"size mismatch remote={o.strip()}")
        except Exception as exc:
            print(f"attempt {i} failed: {exc}")
        time.sleep(5)
        cli = connect()
        sftp = cli.open_sftp()
    return False


def main():
    make_archive()
    cli = connect()
    run(cli, "mkdir -p /srv/ugos/store /srv/ugos/updates")
    if not upload_with_retry(cli):
        sys.exit("upload failed after retries")
    cmds = [
        "cd /srv/ugos/store && tar xzf ../store-public.tar.gz && ls packages | wc -l",
        "rm /srv/ugos/store-public.tar.gz",
    ]
    for c in cmds:
        code, o, e = run(cli, c)
        print(f"$ {c}\n{o}{e}")
    conf = """server {
    listen 80;
    server_name ugospro.135246.xyz;
    root /srv/ugos/store/public;
    index index.html;
    location /updates/ { alias /srv/ugos/updates/; autoindex on; }
}
"""
    sftp = cli.open_sftp()
    sftp.open("/etc/nginx/sites-available/ugos", "w").write(conf)
    run(cli, "ln -sf /etc/nginx/sites-available/ugos /etc/nginx/sites-enabled/ugos && rm -f /etc/nginx/sites-enabled/default && nginx -t && systemctl reload nginx")
    code, o, e = run(cli, "certbot --nginx -d ugospro.135246.xyz --non-interactive --agree-tos -m admin@135246.xyz --redirect 2>&1 | tail -6", timeout=300)
    print("CERTBOT:\n" + (o or e))
    code, o, _e = run(cli, "curl -s https://ugospro.135246.xyz/store/repo.json | head -c 120")
    print("HTTPS check:", o)
    cli.close()


if __name__ == "__main__":
    main()
