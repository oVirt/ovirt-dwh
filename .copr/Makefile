.PHONY: installdeps srpm

installdeps:
	dnf -y install git make

srpm: installdeps
	$(eval SUFFIX=$(shell sh -c " echo '.git$$(git rev-parse --short HEAD)'"))
	mkdir -p tmp.repos/SOURCES
	make dist
	rpmbuild \
		-D "_topdir tmp.repos" \
		-D "release_suffix ${SUFFIX}" \
		-ts ./*.tar.gz
	cp tmp.repos/SRPMS/*.src.rpm $(outdir)
