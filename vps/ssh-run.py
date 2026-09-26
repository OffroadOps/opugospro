import os
import sys
import json
import sys

import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD


def run(cmds):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
    out = {}
    for c in cmds:
        _, stdout, stderr = cli.exec_command(c, timeout=120)
        o = stdout.read().decode("utf-8", errors="replace")
        e = stderr.read().decode("utf-8", errors="replace")
        out[c] = (o + ("\n[stderr] " + e if e.strip() else "")).strip()
    cli.close()
    return out


if __name__ == "__main__":
    cmds = sys.argv[1:]
    for c, r in run(cmds).items():
        print(f"$ {c}\n{r}\n{'='*60}")
