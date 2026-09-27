import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

FIX = r'''
set -e
cd /etc/ugos-ca
openssl req -new -key mock.key -subj "/CN=api-zh.ugnas.com" -out mock.csr
openssl x509 -req -in mock.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out mock.crt -days 1825 -extfile mock.cnf
openssl x509 -in mock.crt -noout -text | grep -A2 "Alternative"
'''
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
_o, out, err = cli.exec_command(FIX, timeout=60)
print(out.read().decode())
e = err.read().decode()
if e.strip():
    print("ERR:", e[-300:])
cli.close()
