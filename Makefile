all: build

rpmrelease=1
rpmversion=3.0.0
RPMTOP=$(shell bash -c "pwd -P")/rpmtop
NAME=ovirt-dwh


TARBALL=$(NAME)-$(rpmversion).tar.gz
SRPM=$(RPMTOP)/SRPMS/$(NAME)-$(rpmversion)-$(rpmrelease)*.src.rpm

.PHONY: tarball
tarball: $(TARBALL)
$(TARBALL):
	git archive --format=tar HEAD | gzip > $(TARBALL)

.PHONY: srpm rpm
srpm: $(SRPM)
$(SRPM): $(TARBALL)
	sed 's/^Version:.*/Version: $(rpmversion)/;s/^Release:.*/Release: $(rpmrelease)%{dist}/;s/%{release}/$(rpmrelease)/' packaging/$(NAME).spec.in > $(NAME).spec
	mkdir -p $(RPMTOP)/{RPMS,SRPMS,SOURCES,BUILD}
	rpmbuild -bs \
	    --define="_topdir $(RPMTOP)" \
	    --define="_sourcedir ." $(NAME).spec

rpm: $(SRPM)
	rpmbuild --define="_topdir $(RPMTOP)" --rebuild $<

build:
	mvn clean install -Dproject.build.sourceEncoding=ISO-8859-1

clean:
	$(RM) *~ *.pyc $(NAME)*.tar.gz $(NAME).spec
	$(RM) -r rpmtop
