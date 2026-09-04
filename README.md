# csv

CSV to html with python.

## Installation

Installation on debian (default python libraries are used):

```bash
# Caddy is preinstalled in my example
sudo apt install git -y
sudo useradd -m -d /opt/csv csv


# as csv user
su csv
cd
git clone https://github.com/AveragePaintEnjoyer/csv.git
exit

# Caddy config edit
nano /etc/caddy/Caddyfile
systemctl restart caddy
```

Caddy config snippet:

```conf
ur.doma.in {
    root * /opt/csv/csv/public
    try_files {path} {path}.html
    file_server

    log {
        output file /var/log/caddy/web.log
        format json
    }

    handle_errors {
        rewrite * /404.html
        file_server
    }

    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "no-referrer"
        Content-Security-Policy "
            default-src 'self';
            script-src 'self' 'unsafe-inline';
            style-src 'self' 'unsafe-inline';
            img-src 'self' data:;
            object-src 'none';
            base-uri 'self';
            frame-ancestors 'none';
        "
        -Server
    }
}
```