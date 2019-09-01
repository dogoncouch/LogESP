# LogESP Installation
LogESP (c) 2018 Dan Persons | [MIT License](../LICENSE)

- Tested on:
  - Ubuntu server 16.04
  - Ubuntu server 18.04

## Index

- [Requirements](#requirements)
- [MariaDB Setup](#mariadb-setup)
- [LogESP Setup](#logesp-setup)
- [Rsyslog Setup](#rsyslog-setup)
- [Nginx Setup](#nginx-setup)
- [Edit rc.local](#edit-rclocal)
- [Reboot](#reboot)
- [Extras](#extras)
  - [Updating](#updating)
  - [Production Environments](#production-environments)
  - [Distributed Environments](#distributed-environments)

Note: This installation is intended for development, and trying out the software. In production environments, LogESP should be configured by a professional with experience securing production servers.

## Requirements
On small home networks, LogESP can be run on an ubuntu server virtual machine with less than half of a processor, 1.5G of memory, and 8G of disk space.
```
apt update ; apt upgrade
apt install build-essential python3-dev python3-venv libmysqlclient-dev mariadb-server nginx ntp
```
Notes: On some Debian derived Linux distros, you may need to replace `libmysqlclient-dev` with `default-libmysqlclient-dev` and additionally install `git` for these instructions to work.

## Mariadb Setup
```
systemctl enable --now mysql
mysql_secure_installation
mysql -u root -p
```
Note: Change the password below (IDENTIFIED BY). Even though it's localhost.
```
CREATE DATABASE siem_data CHARACTER SET UTF8;
CREATE USER logespctrl@localhost IDENTIFIED BY 'siems2bfine';
USE siem_data;
GRANT ALL PRIVILEGES ON siem_data.* TO logespctrl@localhost;
FLUSH PRIVILEGES;
exit
```

## LogESP Setup
### Clone LogESP
```
cd /opt
git clone https://github.com/dogoncouch/LogESP.git
cd LogESP
```

### Create virtual env
```
python3 -m venv /opt/LogESP/env
source env/bin/activate
pip install -r requirements.txt
```

### Add logespd User
```
useradd -r -d /opt/LogESP -s /sbin/nologin -U logespd
gpasswd -a logespd adm
```

### Link daemon scripts
```
ln -s /opt/LogESP/scripts/logesp /usr/local/bin
ln -s /opt/LogESP/scripts/logespd.service /lib/systemd/system
ln -s /opt/LogESP/scripts/logesp-uwsgi.service /lib/systemd/system
systemctl enable logespd
systemctl enable logesp-uwsgi
```

### Update Permissions
```
cp /opt/LogESP/config/db.conf.example /opt/LogESP/config/db.conf
chown logespd.www-data /opt/LogESP/config/db.conf
chmod 640 /opt/LogESP/config/db.conf
cp /opt/LogESP/config/parser.conf.example /opt/LogESP/config/parser.conf
chown root.logespd /opt/LogESP/config/parser.conf
chmod 640 /opt/LogESP/config/parser.conf
cp config/settings.py.example config/settings.py
chown logespd.www-data config/settings.py
chmod 640 config/settings.py
chown -R logespd.www-data /opt/LogESP/run
chmod 770 run
```

### Edit config/settings.py
- Add server IP/FQDN to `ALLOWED_HOSTS`
- Update `TIME_ZONE` setting

### Edit config/db.conf
- Update username, password

### Edit config/parser.conf
- Uncomment necessary files
- Add more files, if necessary

### Set Up Static Files, Database
- Set up database, collect static files:
```
make newdb
make staticfiles
```
Note: When confirming static file collection, you must type `yes`, not `y`.

## Rsyslog Setup
### Place Files
```
cp /opt/LogESP/config/rsyslog/server/*.conf /etc/rsyslog.d/
mkdir /var/log/uwsgi
touch /var/log/cisco.log /var/log/snort.log /var/log/audit.log /var/log/windows.log /var/log/uwsgi/logesp.log
chown -R syslog.adm /var/log/uwsgi /var/log/cisco.log /var/log/snort.log /var/log/audit.log /var/log/windows.log
```
This configuration uses a UDP server. In a production environment, using a TCP syslog server with public key infrastructure integration is recommended. Log sources that require UDP should communicate out of band (i.e. on a management network).

## Nginx Setup
### Create Links
```
cp /opt/LogESP/config/nginx/logesp_nginx.conf.example /opt/LogESP/config/nginx/logesp_nginx.conf
ln -s /opt/LogESP/config/nginx/logesp_nginx.conf /etc/nginx/sites-enabled/
```

### Create SSL Certificate
```
mkdir /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096
```
In a production environment, use an SSL certificate signed by your CA.

### Set Server Name
- Edit `/opt/LogESP/config/nginx/logesp_nginx.conf`, and replace `0.0.0.0` with your server FQDN or IP address.
- If you are going to be using a trusted certificate, uncomment the line that starts with `add_header Strict-Transport-Security`.

### Set PID File Permissions
```
touch /opt/LogESP/run/logesp-uwsgi-master.pid
chown www-data.www-data /opt/LogESP/run/logesp-uwsgi-master.pid
chmod 644 /opt/LogESP/run/logesp-uwsgi-master.pid
```

## Reboot
```
reboot
```

## Extras
### Updating
Run `make update` to update pip dependencies, pull changes from GitHub, and restart LogESP. Run `make update-logesp` to skip dependency updates.

### Production Environments
In a production security environment, a few more steps are recommended:
- Use an SSL certificate signed by your CA
- Use NTP on log sources for time synchronization
- Secure NTP communication
- Update the `SECRET_KEY` setting in `config/settings.py`
- Follow all other instructions in the [Django deployment checklist](https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/)

Note: LogESP is still testing, and should only be deployed in production by people who really know what they are doing.

### Distributed Environments
Event parsing can be distributed among multiple syslog servers, if necessary. Adding the `-p` option to the `logesp` command in `/etc/rc.local` on all but the main server will avoid redundant rule checking. Using MariaDB with SSL is recommended.

A few extra precautions are recommended:
- Use separate MariaDB credentials (with minimal permissions) on servers
  - Web servers don't need to add, change, or delete log events or rule events
  - Parsing servers only need to do the following:
    - Read parsers and parse helpers
    - Create log events
  - Sentry servers only need to do the following:
    - Read limit rules and log/rule events
    - Create rule events
- Use SSL for MariaDB communication
- Use access control lists to minimize exposure
