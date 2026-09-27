import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()


def run(cmd, timeout=120):
    _o, out, err = cli.exec_command(cmd, timeout=timeout)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    print(f"$ {cmd[:70]}\n{o.strip()[:600]}{('[err] ' + e.strip()[:300]) if e.strip() else ''}\n")
    return o


# remove the broken sed line from nginx.conf
run("sed -i '/mock_detail/d' /etc/nginx/nginx.conf")
# put log_format into the mock site config itself (server-less context valid inside http? no -
# log_format must live in http context; simplest: use a dedicated include file placed in conf.d)
LOGFMT = 'log_format mock_detail \'REQ=[$request] AK=[$arg_ak] SIGN=[$arg_sign] TS=[$arg_ts] BODY=[$request_body]\';\n'
with sftp.open("/etc/nginx/conf.d/ugos-mock-log.conf", "w") as f:
    f.write(LOGFMT)
run("nginx -t 2>&1 | tail -1 && systemctl reload nginx && systemctl status nginx | head -3 | tail -1")
run("curl -sk https://127.0.0.1/ -H 'Host: api-zh.ugnas.com' | head -c 140; echo")
run("tail -2 /var/log/ugos-mock-access.log 2>/dev/null")
cli.close()
