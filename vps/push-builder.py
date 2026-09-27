import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()
sftp.put(r"H:\ugos\base\scripts\build-ugos-arm-image.py", "/srv/ugos/opugospro/base/scripts/build-ugos-arm-image.py")
print("builder uploaded")
_o, out, err = cli.exec_command("pkill -f build-ugos-arm-image 2>/dev/null; cd /srv/ugos/opugospro && nohup python3 -u base/scripts/build-ugos-arm-image.py --profile base/profiles/radxa-cubie-a5e/profile.json --payload-dir /srv/ugos/payload-mix/payload --core-preinstall /srv/ugos/build-inputs/core-preinstall.tar.gz > /tmp/v12-build.log 2>&1 < /dev/null & echo relaunched", timeout=15)
print(out.read().decode())
cli.close()
