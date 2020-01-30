# ====================================================================
#
#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ====================================================================
#
# This software consists of voluntary contributions made by many
# individuals on behalf of the Apache Software Foundation.  For more
# information on the Apache Software Foundation, please see
# <http://www.apache.org/>.

#
# CUSTOMIZATION-BEGIN
#
EXTRA_BUILD_FLAGS=
BUILD_VALIDATION=1

PACKAGE_NAME=ovirt-engine-dwh
ANT=ant
PYTHON=python
PYTHON3=$(shell which python3 2> /dev/null)
PYFLAKES=pyflakes
PEP8=pep8
PREFIX=/usr/local
LOCALSTATE_DIR=$(PREFIX)/var
BIN_DIR=$(PREFIX)/bin
SYSCONF_DIR=$(PREFIX)/etc
DATAROOT_DIR=$(PREFIX)/share
MAN_DIR=$(DATAROOT_DIR)/man
DOC_DIR=$(DATAROOT_DIR)/doc
PKG_DATA_DIR=$(DATAROOT_DIR)/ovirt-engine-dwh
JAVA_DIR=$(DATAROOT_DIR)/java
PKG_SYSCONF_DIR=$(SYSCONF_DIR)/ovirt-engine-dwh
PKG_JAVA_LIB=$(PKG_DATA_DIR)/lib
PKG_CACHE_DIR=$(LOCALSTATE_DIR)/cache/ovirt-engine-dwh
PKG_LOG_DIR=$(LOCALSTATE_DIR)/log/ovirt-engine-dwh
PKG_TMP_DIR=$(LOCALSTATE_DIR)/tmp/ovirt-engine-dwh
PKG_STATE_DIR=$(LOCALSTATE_DIR)/lib/ovirt-engine-dwh
PYTHON_DIR=$(PYTHON_SYS_DIR)
PYTHON3_DIR=$(PYTHON3_SYS_DIR)
DEV_PYTHON_DIR=
DEV_PYTHON3_DIR=
PKG_USER=ovirt
PKG_GROUP=ovirt
#
# CUSTOMIZATION-END
#

include version.mak
RPM_VERSION=$(VERSION)
PACKAGE_VERSION=$(VERSION)$(if $(MILESTONE),_$(MILESTONE))
DISPLAY_VERSION=$(PACKAGE_VERSION)
DWH_VERSION=$(VERSION)

BUILD_FLAGS:=$(BUILD_FLAGS) $(EXTRA_BUILD_FLAGS)

PYTHON_SYS_DIR:=$(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib as f;print(f())")
ifneq ($(PYTHON3),)
PYTHON3_SYS_DIR:=$(shell $(PYTHON3) -c "from distutils.sysconfig import get_python_lib as f;print(f())")
endif

TARBALL=$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.gz
BUILD_FILE=tmp.built

.SUFFIXES:
.SUFFIXES: .in

.in:
	sed \
	-e "s|@PKG_USER@|$(PKG_USER)|g" \
	-e "s|@PKG_GROUP@|$(PKG_GROUP)|g" \
	-e "s|@DATAROOT_DIR@|$(DATAROOT_DIR)|g" \
	-e "s|@PKG_SYSCONF_DIR@|$(PKG_SYSCONF_DIR)|g" \
	-e "s|@PKG_DATA_DIR@|$(PKG_DATA_DIR)|g" \
	-e "s|@PKG_LOG_DIR@|$(PKG_LOG_DIR)|g" \
	-e "s|@PKG_STATE_DIR@|$(PKG_STATE_DIR)|g" \
	-e "s|@PKG_JAVA_LIB@|$(PKG_JAVA_LIB)|g" \
	-e "s|@DEV_PYTHON_DIR@|$(DEV_PYTHON_DIR)|g" \
	-e "s|@DEV_PYTHON3_DIR@|$(DEV_PYTHON3_DIR)|g" \
	-e "s|@DWH_VARS@|$(PKG_SYSCONF_DIR)/ovirt-engine-dwhd.conf|g" \
	-e "s|@DWH_DEFAULTS@|$(PKG_DATA_DIR)/services/ovirt-engine-dwhd/ovirt-engine-dwhd.conf|g" \
	-e "s|@RPM_VERSION@|$(RPM_VERSION)|g" \
	-e "s|@RPM_RELEASE@|$(RPM_RELEASE)|g" \
	-e "s|@PACKAGE_NAME@|$(PACKAGE_NAME)|g" \
	-e "s|@PACKAGE_VERSION@|$(PACKAGE_VERSION)|g" \
	-e "s|@DISPLAY_VERSION@|$(DISPLAY_VERSION)|g" \
	-e "s|@DWH_VERSION@|$(DWH_VERSION)|g" \
	-e "s|@VERSION_MAJOR@|$(VERSION_MAJOR)|g" \
	-e "s|@VERSION_MINOR@|$(VERSION_MINOR)|g" \
	-e "s|@VERSION_PATCH_LEVEL@|$(VERSION_PATCH_LEVEL)|g" \
	-e "s|@PEP8@|$(PEP8)|g" \
	-e "s|@PYFLAKES@|$(PYFLAKES)|g" \
	$< > $@

GENERATED = \
	build/python-check.sh \
	ovirt-engine-dwh.spec \
	packaging/etc/ovirt-engine-dwhd.conf.d/README \
	packaging/bin/dwh-prolog.sh \
	packaging/services/ovirt-engine-dwhd/config.py \
	packaging/services/ovirt-engine-dwhd/ovirt-engine-dwhd.conf \
	packaging/services/ovirt-engine-dwhd/ovirt-engine-dwhd.systemd \
	packaging/services/ovirt-engine-dwhd/ovirt-engine-dwhd.sysv \
	packaging/services/ovirt-engine-dwhd/ovirt_engine_dwh_watchdog.cron \
	packaging/setup/ovirt_engine_setup/dwh/config.py \
	packaging/sys-etc/logrotate.d/ovirt-engine-dwhd \
	$(NULL)

all:	\
	generated-files \
	validations \
	$(BUILD_FILE) \
	$(NULL)

generated-files:	$(GENERATED)
	chmod a+x build/python-check.sh
	chmod a+x packaging/services/ovirt-engine-dwhd/ovirt-engine-dwhd.sysv
	chmod a+x packaging/services/ovirt-engine-dwhd/ovirt_engine_dwh_watchdog.cron

$(BUILD_FILE):
	$(ANT) $(BUILD_FLAGS) all
	touch $(BUILD_FILE)

clean:
	$(ANT) $(BUILD_FLAGS) clean
	rm -rf $(BUILD_FILE)
	rm -rf tmp.dev.flist
	rm -rf $(GENERATED)

install: \
	all \
	install-artifacts \
	install-layout \
	$(NULL)

.PHONY: ovirt-engine-dwh.spec.in

dist:	ovirt-engine-dwh.spec
	git ls-files | tar --files-from /proc/self/fd/0 -czf "$(TARBALL)" ovirt-engine-dwh.spec
	@echo
	@echo For distro specific packaging refer to http://www.ovirt.org/Build_Binary_Package
	@echo

# copy SOURCEDIR to TARGETDIR
# exclude EXCLUDEGEN a list of files to exclude with .in
# exclude EXCLUDE a list of files.
copy-recursive:
	( cd "$(SOURCEDIR)" && find . -type d -printf '%P\n' ) | while read d; do \
		install -d -m 755 "$(TARGETDIR)/$${d}"; \
	done
	( \
		cd "$(SOURCEDIR)" && find . -type f -printf '%P\n' | \
		while read f; do \
			exclude=false; \
			for x in $(EXCLUDE_GEN); do \
				if [ "$(SOURCEDIR)/$${f}" = "$${x}.in" ]; then \
					exclude=true; \
					break; \
				fi; \
			done; \
			for x in $(EXCLUDE); do \
				if [ "$(SOURCEDIR)/$${f}" = "$${x}" ]; then \
					exclude=true; \
					break; \
				fi; \
			done; \
			$${exclude} || echo "$${f}"; \
		done \
	) | while read f; do \
		src="$(SOURCEDIR)/$${f}"; \
		dst="$(TARGETDIR)/$${f}"; \
		[ -x "$${src}" ] && MASK=0755 || MASK=0644; \
		[ -n "$(DEV_FLIST)" ] && echo "$${dst}" | sed 's#^$(PREFIX)/##' >> "$(DEV_FLIST)"; \
		install -T -m "$${MASK}" "$${src}" "$${dst}"; \
	done

validations:	generated-files
	if [ "$(BUILD_VALIDATION)" != 0 ]; then \
		build/shell-check.sh && \
		build/python-check.sh; \
	fi

install-artifacts:
	install -d -m 755 "$(DESTDIR)$(PKG_JAVA_LIB)"
	for jar in lib/*.jar; do \
		install -m 0644 "$${jar}" "$(DESTDIR)$(PKG_JAVA_LIB)"; \
	done

install-packaging-files: \
		$(GENERATED) \
		$(NULL)
	$(MAKE) copy-recursive SOURCEDIR=packaging/sys-etc TARGETDIR="$(DESTDIR)$(SYSCONF_DIR)" EXCLUDE_GEN="$(GENERATED)"
	$(MAKE) copy-recursive SOURCEDIR=packaging/etc TARGETDIR="$(DESTDIR)$(PKG_SYSCONF_DIR)" EXCLUDE_GEN="$(GENERATED)"
	$(MAKE) copy-recursive SOURCEDIR=packaging/setup TARGETDIR="$(DESTDIR)$(PKG_DATA_DIR)/../ovirt-engine/setup" EXCLUDE_GEN="$(GENERATED)"
	for d in bin conf dbscripts etl services wildflydom4jjavaconf; do \
		$(MAKE) copy-recursive SOURCEDIR="packaging/$${d}" TARGETDIR="$(DESTDIR)$(PKG_DATA_DIR)/$${d}" EXCLUDE_GEN="$(GENERATED)"; \
	done

install-layout: \
		install-packaging-files \
		$(NULL)

	install -dm 755 "$(DESTDIR)$(PKG_STATE_DIR)/backups"

	install -d -m 755 "$(DESTDIR)$(BIN_DIR)"
	ln -sf "$(PKG_DATA_DIR)/bin/dwh-vacuum.sh" "$(DESTDIR)$(BIN_DIR)/dwh-vacuum"

all-dev:
	rm -f $(GENERATED)
	$(MAKE) \
		all \
		DEV_PYTHON_DIR="$(PREFIX)$(PYTHON_SYS_DIR)" \
		DEV_PYTHON3_DIR="$(PREFIX)$(PYTHON3_SYS_DIR)" \
		$(NULL)

install-dev:	\
		all-dev \
		$(NULL)

	# remove dbscripts to avoid dups
	rm -fr "$(DESTDIR)$(PKG_DATA_DIR)/dbscripts"

	if [ -f "$(DESTDIR)$(PREFIX)/dev.$(PACKAGE_NAME).flist" ]; then \
		cat "$(DESTDIR)$(PREFIX)/dev.$(PACKAGE_NAME).flist" | while read f; do \
			rm -f "$(DESTDIR)$(PREFIX)/$${f}"; \
		done; \
		rm -f "$(DESTDIR)$(PREFIX)/dev.$(PACKAGE_NAME).flist"; \
	fi

	rm -f tmp.dev.flist
	$(MAKE) \
		install \
		BUILD_VALIDATION=0 \
		PYTHON_DIR="$(PREFIX)$(PYTHON_SYS_DIR)" \
		PYTHON3_DIR="$(PREFIX)$(PYTHON3_SYS_DIR)" \
		DEV_FLIST=tmp.dev.flist \
		$(NULL)
	cp tmp.dev.flist "$(DESTDIR)$(PREFIX)/dev.$(PACKAGE_NAME).flist"

	install -d "$(DESTDIR)$(PKG_STATE_DIR)"
	install -d "$(DESTDIR)$(PKG_LOG_DIR)"
