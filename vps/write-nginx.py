import os
import sys
import paramiko

HOST = "5.181.177.120"
USER = "root"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vps_config import PASSWORD

CONF = """server {
    listen 80;
    server_name ugospro.135246.xyz;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name ugospro.135246.xyz;
    root /www;
    autoindex on;
    index index.html;

    ssl_certificate /etc/letsencrypt/live/ugospro.135246.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ugospro.135246.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /updates/ {
        alias /srv/ugos/updates/;
        autoindex on;
    }
}
"""

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(HOST, username=USER, password=PASSWORD, timeout=20)
cli.open_sftp().open("/etc/nginx/sites-available/ugos", "w").write(CONF)
_o, out, err = cli.exec_command("ls /etc/letsencrypt/live/ugospro.135246.xyz/ && nginx -t 2>&1 | tail -1 && systemctl reload nginx && sleep 1 && ss -tlnp | grep -E ':443|:80'")
print(out.read().decode(), err.read().decode())
cli.close()
