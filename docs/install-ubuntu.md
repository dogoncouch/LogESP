# LDSI Installation
LogDissect Security Intelligence (c) 2018 Dan Persons | [MIT License](../LICENSE)

- Ubuntu server 16.04

## Index

- [Requirements](#requirements)
- [MariaDB Setup](#mariadb-setup)
- [LDSI Setup](#ldsi-setup)
- [Rsyslog Setup](#rsyslog-setup)
- [Nginx Setup](#nginx-setup)
- [Edit rc.local](#edit-rclocal)
- [Reboot](#reboot)
- [Extras](#extras)
  - [Production Environments](#production-environments)
  - [Distributed Environments](#distributed-environments)

Note: This installation is intended for development, and trying out the software. In production environments, LDSI should be configured by a professional with experience securing production servers.

## Requirements
On small home networks, LDSI can be run on an ubuntu server virtual machine with less than half of a processor, 1.5G of memory, and 8G of disk space.
```
apt update ; apt upgrade
apt install build-essential python3-dev python3-venv libmysqlclient-dev mariadb-server nginx ntp
```

## Mariadb Setup
```
systemctl enable --now mysql
mysql_secure_installation
mysql -u root -p
```
Note: Change the password below (IDENTIFIED BY). Even though it's localhost.
```
CREATE DATABASE siem_data CHARACTER SET UTF8;
CREATE USER ldsictrl@localhost IDENTIFIED BY 'siems2bfine';
GRANT ALL PRIVILEGES ON siem_data TO ldsictrl@localhost;
FLUSH PRIVILEGES;
exit
```

## LDSI Setup
### Clone LDSI
```
cd /opt
git clone https://github.com/dogoncouch/ldsi.git
cd ldsi
```

### Create virtual env
```
cd /opt
python3 -m venv .
source bin/activate
pip install requirements.txt
```

### Add ldsid User
```
useradd -r -d /opt/ldsi -s /sbin/nologin -U ldsid
```

### Set Up Static Files, Database
- Set up database, collect static files:
```
make new-db
make static
```

### Edit config/settings.py
- Add server IP/FQDN to `ALLOWED_HOSTS`
- Update `TIME_ZONE` setting

### Edit config/db.conf
- Update username, password
- Update file permissions

### Edit config/parser.conf
- Uncomment necessary files
- Add more files, if necessary

### Link ldsi daemon to /usr/local/bin
```
ln -s /opt/ldsi/scripts/ldsi /usr/local/bin
```

### Update Permissions
```
chgrp -R ldsid /opt/ldsi
chown ldsid.www-data /opt/ldsi/config/db.conf
chmod 640 /opt/ldsi/config/db.conf
chmod 640 /opt/ldsi/config/parser.conf
chown ldsid.www-data /opt/ldsi/run
chmod 664 /opt/ldsi/run
```

## Rsyslog Setup
### Place Files
```
cp /opt/ldsi/config/rsyslog/10-server.conf /etc/rsyslog.d/
cp /opt/ldsi/config/rsyslog/70-cisco.conf /etc/rsyslog.d/
cp /opt/ldsi/config/rsyslog/71-daemon.conf /etc/rsyslog.d/
cp /opt/ldsi/config/rsyslog/75-snort.conf /etc/rsyslog.d/
cp /opt/ldsi/config/rsyslog/77-audit.conf /etc/rsyslog.d/
cp /opt/ldsi/config/rsyslog/78-windows.conf /etc/rsyslog.d/
touch /var/log/cisco.log /var/log/snort.log /var/log/audit.log /var/log/windows.log
chown syslog.adm /var/log/cisco.log /var/log/snort.log /var/log/audit.log /var/log/windows.log
```
This configuration uses a UDP server. In a production environment, using a TCP syslog server with public key infrastructure integration is recommended. Log sources that require UDP should communicate out of band (i.e. on a management network).

## Nginx Setup
### Create Links
```
ln -s /opt/ldsi/config/nginx/ldsi_nginx.conf /etc/nginx/sites-enabled/
```

### Create SSL Certificate
```
mkdir /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
```
In a production environment, use SSL certificates signed by your CA.

### Set Server Name
Edit `/opt/ldsi/config/nginx/ldsi_nginx.conf`, and replace `0.0.0.0` with your server FQDN or IP address.

### Set PID File Permissions
```
touch /opt/ldsi/run/ldsi-uwsgi-master.pid
chown www-data.www-data /opt/ldsi/run/ldsi-uwsgi-master.pid
chmod 644 /opt/ldsi/run/ldsi-uwsgi-master.pid
```

## Edit rc.local
- Add the following:
```
/opt/ldsi/scripts/ldsi start
/opt/ldsi/bin/uwsgi --ini /opt/ldsi/config/nginx/ldsi_uwsgi.ini
```

## Reboot
```
reboot
```

## Extras
### Production Environments
In a production security environment, a few more steps are recommended:
- Secure NTP communication
- Use an SSL certificate signed by your CA
- Use NTP on log sources for time synchronization
- Update the `SECRET_KEY` setting in `config/settings.py`
Note: LDSI isn't ready for production environments yet. Use with caution; review all django settings.

### Distributed Environments
Event parsing can be distributed among multiple syslog servers, if necessary. Adding the `-p` option to the `start.sh` command in `/etc/rc.local` on all but the main server will avoid redundant rule checking. Using MariaDB with SSL is recommended.

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
