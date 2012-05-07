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
mkdir -p /var/log/ovirt-engine/ > /dev/null 2>&1
mkdir -p /etc/logrotate.d/ovirt-engine-dwhd > /dev/null 2>&1
mkdir -p /etc/ovirt-engine/ovirt-engine-dwh > /dev/null 2>&1

echo
echo -- Copying history service to /etc/init.d and setting it up --
echo
cp -f ../../../../data-warehouse/history_etl/history_service/ovirt-engine-dwhd /etc/init.d
if [ ${USER} = "root" ]; then
    sed -i "s/\/usr\/share/\/${USER}/g" /etc/init.d/ovirt-engine-dwhd
    sed -i "s/\/usr\/share/\/${USER}/g" /${USER}/ovirt-engine-dwh/etl/history_service.sh
else
    sed -i "s/\/usr\/share/\/home\/${USER}/g" /etc/init.d/ovirt-engine-dwhd
    sed -i "s/\/usr\/share/\/home\/${USER}/g" /home/${USER}/ovirt-engine-dwh/etl/history_service.sh
fi

echo
echo -- Copying log rotate config file to /etc/logrotate.d/ovirt-engine-dwhd --
echo
cp -n ../../../../data-warehouse/history_etl/history_service/ovirt-engine-dwhd.logrotate /etc/logrotate.d/ovirt-engine-dwhd

echo
echo -- Adding history service to linux --
echo
if [ ${USER} = "root" ]; then
    ln -s -f /${USER}/ovirt-engine-dwh/etl/config/Default.properties /etc/ovirt-engine/ovirt-engine-dwh
else
    ln -s -f /home/${USER}/ovirt-engine-dwh/etl/config/Default.properties /etc/ovirt-engine/ovirt-engine-dwh
fi
chmod 744 /etc/init.d/ovirt-engine-dwhd
/sbin/chkconfig --add ovirt-engine-dwhd
/sbin/service ovirt-engine-dwhd stop > /dev/null 2>&1
/usr/sbin/logrotate /etc/logrotate.conf > /dev/null || /bin/true

echo
echo DONE
echo
