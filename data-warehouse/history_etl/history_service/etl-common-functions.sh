#!/bin/sh
#

function procrunning() {
   procid=0
   for procid in `cat /var/run/ovirt/ovirt-dwhd.pid`; do
          ps -fp $procid | grep HistoryETL > /dev/null && pid=$procid
   done
}
