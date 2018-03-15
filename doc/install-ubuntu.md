# LDSI Installation
- Ubuntu server 16.04

## Index

- [Requirements](#requirements)
- [MariaDB Setup](#mariadb-setup)
- [Virtual Environment](#virtual-environment)
- [LDSI Setup](#ldsi-setup)
- [Rsyslog Setup](#rsyslog-setup)
- [Nginx Setup](#nginx-setup)
- [Edit rc.local](#edit-rclocal)
- [Reboot](#reboot)

Note: This installation is intended for development, and trying out the software. In production environments, LDSI should be configured by a professional with experience securing production servers.

## Requirements
```
apt update ; apt upgrade
apt install build-essential python3-dev python3-venv libmysqlclient-dev mariadb-server nginx
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

## Virtual Environment
### Create virtual env
```
cd /opt
python3 -m venv ldsi
cd ldsi
source bin/activate
```

### Virtual env programs
```
pip install django mysqlclient uwsgi
```

## LDSI Setup
### Clone LDSI
```
git clone https://github.com/dogoncouch/ldsi.git
cd ldsi
```

### Set Up Static Files, Database
- Collect static files, set up database:
```
python manage.py collectstatic
make new-db
```

### Edit ldsi/settings.py
- Add host to `ALLOWED_HOSTS`
- Review database settings
- Update `TIME_ZONE` setting

### Edit config/parser.conf
- Uncomment necessary files
- Add more files, if necessary

## Rsyslog Setup
### Place Files
```
cp /opt/ldsi/ldsi/config/rsyslog/10-server.conf /etc/rsyslog.d/
cp /opt/ldsi/ldsi/config/rsyslog/70-cisco.conf /etc/rsyslog.d/
cp /opt/ldsi/ldsi/config/rsyslog/75-snort.conf /etc/rsyslog.d/
cp /opt/ldsi/ldsi/config/rsyslog/76-uselog.conf /etc/rsyslog.d/
cp /opt/ldsi/ldsi/config/rsyslog/77-audit.conf /etc/rsyslog.d/
cp /opt/ldsi/ldsi/config/rsyslog/78-windows.conf /etc/rsyslog.d/
touch /var/log/cisco.log /var/log/snort.log /var/log/audit.log /var/log/windows.log
chown syslog.admin /var/log/cisco.log /var/log/snort.log /var/log/audit.log /var/log/windows.log
```

## Nginx Setup
### Create Links
```
ln -s /opt/ldsi/ldsi/config/nginx/ldsi_nginx.conf /etc/nginx/sites-enabled/
```

### Create SSL Certificate
```
mkdir /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
```
In a production environment, use SSL certificates signed by your CA.

## Edit rc.local
```
/opt/ldsi/ldsi/start.sh -b /opt/ldsi/ldsi -e /opt/ldsi & >> /dev/null
/opt/ldsi/bin/uwsgi --ini /opt/ldsi/ldsi/config/nginx/ldsi_uwsgi.ini
```

## Reboot
```
reboot
```
