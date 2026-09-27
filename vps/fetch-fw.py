"""Download the latest official arm64 firmware for product 27 (DHP4300 Plus, rk3588) onto the VPS."""
import json
import re
import subprocess
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}

# fresh temp link (the old ones expire)
import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
cmd = "curl -s 'https://api-zh.ugnas.com/api/system/v1/ua/temp/link?appType=firmware&id=7213&model=27'"
_o, out, _e = cli.exec_command(cmd, timeout=60)
j = json.loads(out.read().decode())
temp = j["data"]["linkData"]["tempUrl"]
fname = temp.split("?")[0].rsplit("/", 1)[-1]
print("tempUrl resolved ->", fname)
cli.close()

# download on the VPS (server-side, fast pipe to UGREEN CDN)
dl = (
    "cd /srv/ugos/official-fw && "
    f"curl -sL --retry 3 -C - -o '{fname}' '{temp}' ; "
    "ls -la /srv/ugos/official-fw/"
)
_o, out, err = cli_connect = None, None, None
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
cli.exec_command("mkdir -p /srv/ugos/official-fw")
_o, out, _e = cli.exec_command(dl, timeout=3000)
print(out.read().decode()[-600:])
cli.close()
