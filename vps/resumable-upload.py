"""Resumable SFTP upload for the flaky VPS link: seek-based continuation with retries."""
import os
import sys
import time

import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD


def connect():
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
    return cli


def resumable_put(cli, local: str, remote: str):
    sftp = cli.open_sftp()
    lsize = os.path.getsize(local)
    try:
        roffset = sftp.stat(remote).st_size
    except FileNotFoundError:
        roffset = 0
    attempts = 0
    while roffset < lsize:
        attempts += 1
        if attempts > 200:
            raise RuntimeError("too many retries")
        try:
            with open(local, "rb") as f:
                f.seek(roffset)
                if roffset:
                    print(f"resuming at {roffset:,}/{lsize:,} ({roffset*100//lsize}%)", flush=True)
                with sftp.open(remote, "ab") as r:
                    r.set_pipelined(False)
                    while True:
                        chunk = f.read(512 * 1024)
                        if not chunk:
                            break
                        r.write(chunk)
            roffset = sftp.stat(remote).st_size
        except Exception as exc:
            print(f"interrupted at {roffset:,}: {type(exc).__name__}", flush=True)
            time.sleep(4)
            cli.close()
            cli = connect()
            sftp = cli.open_sftp()
            try:
                roffset = sftp.stat(remote).st_size
            except FileNotFoundError:
                roffset = 0
    print(f"upload complete: {remote} = {lsize:,} bytes", flush=True)
    return cli


def main():
    local, remote = sys.argv[1], sys.argv[2]
    cli = connect()
    cli.exec_command(f"mkdir -p {os.path.dirname(remote)}")
    time.sleep(1)
    cli = resumable_put(cli, local, remote)
    _c, out, _e = cli.exec_command(f"stat -c %s {remote}")
    size = out.read().decode().strip()
    ok = size == str(os.path.getsize(local))
    print(f"final size check: remote={size} local={os.path.getsize(local)} -> {'OK' if ok else 'MISMATCH'}")
    cli.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
