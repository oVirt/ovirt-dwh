# oVirt Engine Data Warehouse
[![Copr build status](https://copr.fedorainfracloud.org/coprs/ovirt/ovirt-master-snapshot/package/ovirt-engine-dwh/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ovirt/ovirt-master-snapshot/package/ovirt-engine-dwh/)

Welcome to the oVirt Engine Data Warehouse source repository.

This repository is hosted on [gerrit.ovirt.org:ovirt-dwh](https://gerrit.ovirt.org/#/admin/projects/ovirt-dwh)
and a **backup** of it is hosted on [GitHub:ovirt-dwh](https://github.com/oVirt/ovirt-dwh)


## How to contribute

### ETL Project Development

To open the talend ETL project:
1. Download Talend's Open Studio v4.2.2 from www.talend.com.
2. Import project and open it.
3. Add the PGSQL (postgresql-9.0-801.jdbc4) JDBC jars locations to the connections in "History ETL 0.1" job.
4. Run and change context; ip, user and password to match the input (ovirt) and output (ovirt_engine_history).


### Submitting patches

Patches are welcome!

Please submit patches to [gerrit.ovirt.org:ovirt-dwh](https://gerrit.ovirt.org/#/admin/projects/ovirt-dwh).
If you are not familiar with the review process for Gerrit patches you can read about [Working with oVirt Gerrit](https://ovirt.org/develop/dev-process/working-with-gerrit.html)
on the [oVirt](https://ovirt.org/) website.

**NOTE**: We might not notice pull requests that you create on Github, because we only use Github for backups.


### Found a bug or documentation issue?
To submit a bug or suggest an enhancement for oVirt Engine Data Warehouse please use
[oVirt Bugzilla for ovirt-engine-dwh product](https://bugzilla.redhat.com/enter_bug.cgi?product=ovirt-engine-dwh).

If you find a documentation issue on the oVirt website please navigate and click "Report an issue on GitHub" in the page footer.


## Still need help?
If you have any other questions, please join [oVirt Users forum / mailing list](https://lists.ovirt.org/admin/lists/users.ovirt.org/) and ask there.
