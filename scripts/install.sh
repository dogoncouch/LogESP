#!/bin/bash

#echo '=== MariaDB info ==='
#while ! [ "${LDSIDBPASS}" = "${LDSIDBPASS1}" ]; do
#    read -sp 'MariaDB Root Password: ' MDBPASS
#    read -sp 'MariaDB Root Password (again): ' MDBPASS1
#done


echo '=== LDSI Database Info ==='
read -p 'DB Instance Name: ' LDSIDBINSTANCE
read -p 'DB Username: ' LDSIDBUSER
LDSIDBPASS='1'
LDSIDBPASS1='1'
while ! [ "${LDSIDBPASS}" = "${LDSIDBPASS1}" ]; do
    read -sp 'DB Password: ' LDSIDBPASS
    read -sp 'DB Password (again): ' LDSIDBPASS1
done

if [ "${LDSIDBPASS}" = "${MDBPASS}" ]; then
    echo "LDSI DB password should not be the MariaDB root password! Exiting."
    exit 1
fi

echo '=== Server Info ==='
read -p 'Server FQDN (or IP): ' LDSISERVERFQDN

# Update apt, install dependencies

# Create mysql database, account

# Create virtual env, get LDSI

# Copy syslog config files, link nginx config, etc

# Set server name in nginx conf/ldsi settings

# Put lines in /etc/rc.local

# Run mysql_secure_installation
# User must input password

# Enable mariadb

# Reboot

