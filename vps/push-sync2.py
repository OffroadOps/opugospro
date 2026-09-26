import os
import sys
import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
cli.open_sftp().put(r"H:\ugos\vps\ugos-sync.py", "/srv/ugos-tools/ugos-sync.py")
_o, out, err = cli.exec_command(
    "mv /srv/ugos/monitor-state.json /srv/ugos/monitor-state.v1.json 2>/dev/null;"
    "systemctl start ugos-sync.service && echo started; sleep 8; systemctl is-active ugos-sync.service; tail -3 /var/log/gen-catalog.log 2>/dev/null",
    timeout=60,
)
# NOTE: read may block if service output holds channel; read what's available
try:
    print(out.read().decode())
except Exception as e:
    print(f"(channel: {e}) — service running detached")
cli.close()
