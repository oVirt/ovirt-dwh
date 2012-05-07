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

echo
echo -- Removing ETL --
echo
/sbin/service ovirt-engine-dwhd stop > /dev/null 2>&1
/sbin/chkconfig --del ovirt-engine-dwhd > /dev/null 2>&1
rm -f /etc/init.d/ovirt-engine-dwhd  > /dev/null 2>&1

echo
echo DONE
echo
