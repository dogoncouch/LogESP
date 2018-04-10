#!/bin/bash

#echo '=== MariaDB info ==='
#while ! [ "${LOGESPDBPASS}" = "${LOGESPDBPASS1}" ]; do
#    read -sp 'MariaDB Root Password: ' MDBPASS
#    read -sp 'MariaDB Root Password (again): ' MDBPASS1
#done

echo "This is an unfinished script."
echo "As a safety precaution, it doesn't work at all"
exit 1

echo '=== LogESP Database Info ==='
read -p 'DB Instance Name: ' LOGESPDBINSTANCE
read -p 'DB Username: ' LOGESPDBUSER
LOGESPDBPASS='1'
LOGESPDBPASS1='1'
while ! [ "${LOGESPDBPASS}" = "${LOGESPDBPASS1}" ]; do
    read -sp 'DB Password: ' LOGESPDBPASS
    read -sp 'DB Password (again): ' LOGESPDBPASS1
done

if [ "${LOGESPDBPASS}" = "${MDBPASS}" ]; then
    echo "LogESP DB password should not be the MariaDB root password! Exiting."
    exit 1
fi

echo '=== Server Info ==='
read -p 'Server FQDN (or IP): ' LOGESPSERVERFQDN

# Update apt, install dependencies

# Create mysql database, account

# Create virtual env, get LogESP

# Copy syslog config files, link nginx config, etc

# Set server name in nginx conf/logesp settings

# Put lines in /etc/rc.local

# Run mysql_secure_installation
# User must input password

# Enable mariadb

# Reboot

