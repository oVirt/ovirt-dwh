#!/bin/bash
#


# ETL functions library.
. /etc/init.d/ovirt-etl

if [ ! -e /usr/share/ovirt-dwh/etl/kill ]; then
    pid=0
    procrunning > /dev/null 2>&1
    if [ $pid = '0' ]; then
        service ovirt-etl start > /dev/null 2>&1
    fi
fi
