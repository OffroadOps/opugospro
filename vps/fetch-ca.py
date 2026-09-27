import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()
sftp.get("/etc/ugos-ca/mock.crt", r"H:\ugos\vps\mock-ca.crt")
_o, out, _e = cli.exec_command("cat /etc/ugos-ca/mock.crt")
crt = out.read().decode()
assert "BEGIN CERTIFICATE" in crt
print("CA cert fetched:", len(crt), "bytes")
print(crt[:200])
cli.close()
