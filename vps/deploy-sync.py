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
sftp = cli.open_sftp()
sftp.put(r"H:\ugos\vps\ugos-sync.py", "/srv/ugos-tools/ugos-sync.py")
print("uploaded ugos-sync.py")

TIMER = """[Unit]
Description=UGOS official firmware monitor/sync

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
"""
SERVICE = """[Unit]
Description=UGOS official firmware monitor/sync
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 -u /srv/ugos-tools/ugos-sync.py
"""
sftp.open("/etc/systemd/system/ugos-sync.service", "w").write(SERVICE)
sftp.open("/etc/systemd/system/ugos-sync.timer", "w").write(TIMER)
_o, out, err = cli.exec_command(
    "systemctl daemon-reload && systemctl enable --now ugos-sync.timer && systemctl start ugos-sync.service && sleep 5 && systemctl is-active ugos-sync.service && journalctl -u ugos-sync.service --no-pager | tail -5",
    timeout=120,
)
print(out.read().decode())
cli.close()
