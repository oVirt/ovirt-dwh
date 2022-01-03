.PHONY: installdeps srpm

installdeps:
	dnf -y install git make

srpm: installdeps
	./.automation/build-srpm.sh
	cp rpmbuild/SRPMS/*.src.rpm $(outdir)
