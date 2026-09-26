import os
import sys
"""Push generator v2 to VPS and run with nohup (channel-safe)."""
import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()
sftp.put(r"H:\ugos\vps\gen-catalog.py", "/srv/ugos-tools/gen-catalog.py")
print("uploaded")
_o, _e, _r = cli.exec_command("pkill -f gen-catalog.py; nohup python3 -u /srv/ugos-tools/gen-catalog.py > /var/log/gen-catalog.log 2>&1 < /dev/null & disown; echo launched", timeout=15)
print(_o.read().decode())
cli.close()
print("running in background on VPS; poll /var/log/gen-catalog.log")
