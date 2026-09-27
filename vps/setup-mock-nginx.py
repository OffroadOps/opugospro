import paramiko

HOST = "5.181.177.120"
USER = "root"
PASSWORD = "yS0IuSXjvWwdgp3HJqP3"

CONF = r'''
# mock UGREEN cloud API endpoints for opugospro boards
server {
    listen 443 ssl;
    http2 on;
    server_name api-zh.ugnas.com center.ugnas.com dl-cn.ugnas.com;

    ssl_certificate /etc/ugos-ca/mock.crt;
    ssl_certificate_key /etc/ugos-ca/mock.key;

    access_log /var/log/ugos-mock-access.log;

    # log every request path+params so we can learn the protocol
    location / {
        access_log /var/log/ugos-mock-access.log mock_detail;
        add_header Content-Type application/json;
        return 200 '{"code":200,"msg":"success","data":{"linkData":{}}}';
    }
}
'''
LOGFMT = '''
log_format mock_detail 'REQ=[$request] UA=[$http_user_agent] AK=[$arg_ak] SIGN=[$arg_sign] TS=[$arg_ts] BODY=[$request_body]';
'''

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
sftp = cli.open_sftp()


def run(cmd, timeout=120):
    _o, out, err = cli.exec_command(cmd, timeout=timeout)
    o = out.read().decode("utf-8", errors="replace")
    e = err.read().decode("utf-8", errors="replace")
    print(f"$ {cmd[:70]}\n{o.strip()[:800]}{('[err] ' + e.strip()[:300]) if e.strip() else ''}\n")
    return o


run("mkdir -p /srv/ugos-mock")
sftp.open("/etc/nginx/snippets/ugos-mock-logfmt.conf", "w").write(LOGFMT)
sftp.open("/etc/nginx/sites-available/ugos-mock", "w").write(CONF)
run("sed -i 's|log_format mock_detail|log_format mock_detail|' /etc/nginx/sites-available/ugos-mock")
# prepend log_format into nginx.conf http block
run("grep -q 'log_format mock_detail' /etc/nginx/nginx.conf || sed -i 's|http {|http {\\n\\tlog_format mock_detail \\'REQ=[$request] AK=[$arg_ak] SIGN=[$arg_sign] TS=[$arg_ts] BODY=[$request_body]\\';|' /etc/nginx/nginx.conf")
run("ln -sf /etc/nginx/sites-available/ugos-mock /etc/nginx/sites-enabled/ugos-mock && nginx -t 2>&1 | tail -1 && systemctl reload nginx && echo mock_nginx_ok")
run("curl -sk https://127.0.0.1/ -H 'Host: api-zh.ugnas.com' | head -c 120; echo")
cli.close()
