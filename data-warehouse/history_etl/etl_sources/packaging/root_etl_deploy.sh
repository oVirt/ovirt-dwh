#!/bin/bash
# Init
FILE="/tmp/out.$$"
GREP="/bin/grep"
#....
# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

USER=${1-text}
[ $# -eq 0 ] && { echo "Usage: $0 user. Please set the user to the one used to deploy the etl with maven." ; exit 1; }
echo "Setting user to $USER..."

set -e

echo
echo -- Creating Directories --
echo
mkdir -p /var/log/ovirt/ > /dev/null 2>&1
mkdir -p /etc/logrotate.d/ovirt-etl > /dev/null 2>&1
mkdir -p /etc/ovirt/ovirt-dwh > /dev/null 2>&1

echo
echo -- Copying history service to /etc/init.d and setting it up --
echo
cp -f ../../../../data-warehouse/history_etl/history_service/ovirt-etl /etc/init.d
sed -i "s/\/usr\/share/\/home\/${USER}/g" /etc/init.d/ovirt-etl
sed -i "s/\/usr\/share/\/home\/${USER}/g" /home/${USER}/ovirt-dwh/etl/history_service.sh

echo
echo -- Copying log rotate config file to /etc/logrotate.d/ovirt-etl --
echo
cp -n ../../../../data-warehouse/history_etl/history_service/ovirt-etl.logrotate /etc/logrotate.d/ovirt-etl

echo
echo -- Adding history service to linux --
echo
ln -s -f /home/${USER}/ovirt-dwh/etl/config/Default.properties /etc/ovirt/ovirt-dwh
chmod 744 /etc/init.d/ovirt-etl
/sbin/chkconfig --add ovirt-etl
/sbin/service ovirt-etl stop > /dev/null 2>&1
/usr/sbin/logrotate /etc/logrotate.conf > /dev/null || /bin/true

echo
echo DONE
echo
