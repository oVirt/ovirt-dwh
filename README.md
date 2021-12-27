# oVirt Engine Data Warehouse
[![Copr build status](https://copr.fedorainfracloud.org/coprs/ovirt/ovirt-master-snapshot/package/ovirt-engine-dwh/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ovirt/ovirt-master-snapshot/package/ovirt-engine-dwh/)

Welcome to the oVirt Engine Data Warehouse source repository. This repository is hosted on [GitHub:ovirt-dwh](https://github.com/oVirt/ovirt-dwh).

## How to contribute

All contributions are welcome - patches, bug reports, and documentation issues.

### ETL Project Development

To open the talend ETL project:
1. Download Talend's Open Studio v4.2.2 from www.talend.com.
2. Import project and open it.
3. Add the PGSQL (postgresql-9.0-801.jdbc4) JDBC jars locations to the connections in "History ETL 0.1" job.
4. Run and change context; ip, user and password to match the input (ovirt) and output (ovirt_engine_history).

### Submitting patches

Please submit patches to [GitHub:ovirt-dwh](https://github.com/oVirt/ovirt-dwh). If you are not familiar with the process, you can read about [collaborating with pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests) on the GitHub website.

### Found a bug or documentation issue?

To submit a bug or suggest an enhancement for oVirt DWH please use [oVirt Bugzilla for ovirt-dwh product](https://bugzilla.redhat.com/enter_bug.cgi?product=ovirt-engine-dwh).

If you don't have a Bugzilla account, you can still report [issues](https://github.com/oVirt/ovirt-dwh/issues). If you find a documentation issue on the oVirt website, please navigate to the page footer and click "Report an issue on GitHub".

## Still need help?

If you have any other questions or suggestions, you can join and contact us on the [oVirt Users forum / mailing list](https://lists.ovirt.org/admin/lists/users.ovirt.org/).
