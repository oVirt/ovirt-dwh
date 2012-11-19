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

MVN=mvn
EXTRA_BUILD_FLAGS=
BUILD_FLAGS=
PACKAGE_NAME=ovirt-engine-dwh
OVIRT_DWH_NAME=$(PACKAGE_NAME)
PREFIX=/usr/local
BIN_DIR=$(PREFIX)/bin
SYSCONF_DIR=$(PREFIX)/etc
DATAROOT_DIR=$(PREFIX)/share
DATA_DIR=$(DATAROOT_DIR)/$(OVIRT_DWH_NAME)
MAVENPOM_DIR=$(DATAROOT_DIR)/maven-poms
JAVA_DIR=$(DATAROOT_DIR)/java
PKG_JAVA_DIR=$(JAVA_DIR)/$(OVIRT_DWH_NAME)
RPMBUILD=rpmbuild
PYTHON=python
PYTHON_DIR:=$(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib as f;print f()")

# RPM version
APP_VERSION:=$(shell cat pom.xml | grep '<ovirt-dwh.version>' | awk -F\> '{print $$2}' | awk -F\< '{print $$1}')
RPM_VERSION:=$(shell echo $(APP_VERSION) | sed "s/-/_/")

# Release Version; used to create y in <x.x.x-y> numbering.
# Should be used to create releases.
RPM_RELEASE_VERSION=1

SPEC_FILE_IN=packaging/ovirt-engine-dwh.spec.in
SPEC_FILE=$(PACKAGE_NAME).spec
OUTPUT_RPMBUILD=$(shell pwd -P)/tmp.rpmbuild
OUTPUT_DIR=output
TARBALL=$(PACKAGE_NAME)-$(RPM_VERSION).tar.gz
SRPM=$(OUTPUT_DIR)/$(PACKAGE_NAME)-$(RPM_VERSION)*.src.rpm
ARCH=noarch
BUILD_FILE=tmp.built
MAVEN_OUTPUT_DIR_DEFAULT=$(shell pwd -P)/tmp.repos
MAVEN_OUTPUT_DIR=$(MAVEN_OUTPUT_DIR_DEFAULT)

ARTIFACTS = \
	historyETLProcedure \
	talendRoutines \
	advancedPersistentLookupLib

all: $(BUILD_FILE)

$(BUILD_FILE):
	export MAVEN_OPTS="${MAVEN_OPTS} -XX:MaxPermSize=512m"
	$(MVN) \
		$(BUILD_FLAGS) \
		$(EXTRA_BUILD_FLAGS) \
		dependency:resolve-plugins
	$(MVN) \
		$(BUILD_FLAGS) \
		$(EXTRA_BUILD_FLAGS) \
		-D skipTests \
		-D altDeploymentRepository=install::default::file://$(MAVEN_OUTPUT_DIR) \
		deploy
	touch $(BUILD_FILE)

clean:
	$(MVN) clean $(EXTRA_BUILD_FLAGS)
	rm -rf $(OUTPUT_RPMBUILD) $(SPEC_FILE) $(OUTPUT_DIR) $(BUILD_FILE)
	[ "$(MAVEN_OUTPUT_DIR_DEFAULT)" = "$(MAVEN_OUTPUT_DIR)" ] && rm -fr "$(MAVEN_OUTPUT_DIR)"

test:
	$(MVN) install $(BUILD_FLAGS) $(EXTRA_BUILD_FLAGS)

install: \
	all \
	install_without_maven

install_without_maven: \
	install_artifacts \
	install_files

tarball:
	sed -e 's/@PACKAGE_VERSION@/$(RPM_VERSION)/g' \
            -e 's/@PACKAGE_RELEASE@/$(RPM_RELEASE_VERSION)/g' $(SPEC_FILE_IN) > $(SPEC_FILE)
	git ls-files | tar --files-from /proc/self/fd/0 -czf $(TARBALL) $(SPEC_FILE)
	rm -f $(SPEC_FILE)
	@echo
	@echo You can use $(RPMBUILD) -tb $(TARBALL) to produce rpms
	@echo

srpm:	tarball
	rm -rf $(OUTPUT_RPMBUILD)
	mkdir -p $(OUTPUT_RPMBUILD)/{SPECS,RPMS,SRPMS,SOURCES,BUILD,BUILDROOT}
	mkdir -p $(OUTPUT_DIR)
	$(RPMBUILD) -ts --define="_topdir $(OUTPUT_RPMBUILD)" $(TARBALL)
	mv $(OUTPUT_RPMBUILD)/SRPMS/*.rpm $(OUTPUT_DIR)
	rm -rf $(OUTPUT_RPMBUILD)
	@echo
	@echo srpm is ready at $(OUTPUT_DIR)
	@echo

rpm:	srpm
	rm -rf $(OUTPUT_RPMBUILD)
	mkdir -p $(OUTPUT_RPMBUILD)/{SPECS,RPMS,SRPMS,SOURCES,BUILD,BUILDROOT}
	mkdir -p $(OUTPUT_DIR)
	$(RPMBUILD) --define="_topdir $(OUTPUT_RPMBUILD)" $(RPMBUILD_EXTRA_ARGS) --rebuild $(SRPM)
	mv $(OUTPUT_RPMBUILD)/RPMS/$(ARCH)/*.rpm $(OUTPUT_DIR)
	rm -rf $(OUTPUT_RPMBUILD)
	@echo
	@echo rpms are ready at $(OUTPUT_DIR)
	@echo

install_artifacts:
	install -dm 755 $(DESTDIR)$(PKG_JAVA_DIR)
	install -dm 755 $(DESTDIR)$(MAVENPOM_DIR)

	for artifact_id in  $(ARTIFACTS); do \
		POM=`find "$(MAVEN_OUTPUT_DIR)" -name "$${artifact_id}-*.pom"`; \
		if ! [ -f "$${POM}" ]; then \
			echo "ERROR: Cannot find artifact $${artifact_id}"; \
			exit 1; \
		fi; \
		JAR=`echo "$${POM}" | sed 's/\.pom/.jar/'`; \
		install -p -m 644 "$${POM}" "$(DESTDIR)$(MAVENPOM_DIR)/$(PACKAGE_NAME)-$${artifact_id}.pom"; \
		[ -f "$${JAR}" ] && install -p -m 644 "$${JAR}" "$(DESTDIR)$(PKG_JAVA_DIR)/$${artifact_id}.jar"; \
	done

install_files:
	install -d $(DESTDIR)$(BIN_DIR)
	install -d $(DESTDIR)$(DATA_DIR)
	install -d $(DESTDIR)$(DATA_DIR)/etl
	install -d $(DESTDIR)$(DATA_DIR)/db-scripts
	install -d $(DESTDIR)$(SYSCONF_DIR)/ovirt-engine/$(OVIRT_DWH_NAME)
	install -d $(DESTDIR)$(SYSCONF_DIR)/cron.hourly
	install -d $(DESTDIR)$(SYSCONF_DIR)/logrotate.d

	install -p -m 755 packaging/$(OVIRT_DWH_NAME)-setup.py $(DESTDIR)$(DATA_DIR)
	install -p -m 755 packaging/common_utils.py $(DESTDIR)$(DATA_DIR)
	install -p -m 755 packaging/decorators.py $(DESTDIR)$(DATA_DIR)
	install -p -m 755 data-warehouse/history_etl/history_service/history_service.sh $(DESTDIR)$(DATA_DIR)/etl
	install -p -m 755 data-warehouse/history_etl/history_service/etl-common-functions.sh $(DESTDIR)$(DATA_DIR)/etl
	cp -a  data-warehouse/history_etl/context_files/* $(DESTDIR)$(DATA_DIR)/etl
	cp -r -a  data-warehouse/historydbscripts_postgres/* $(DESTDIR)$(DATA_DIR)/db-scripts
	install -p -m 660 data-warehouse/history_etl/context_files/ovirt_engine_dwh/historyetl_3_2/contexts/Default.properties $(DESTDIR)$(SYSCONF_DIR)/ovirt-engine/$(OVIRT_DWH_NAME)
	install -p -m 644 packaging/resources/$(OVIRT_DWH_NAME)d.logrotate $(DESTDIR)$(SYSCONF_DIR)/logrotate.d/$(OVIRT_DWH_NAME)d
	install -p -m 755 packaging/resources/ovirt_engine_dwh_watchdog.cron $(DESTDIR)$(SYSCONF_DIR)/cron.hourly

	install -d $(DESTDIR)$(BIN_DIR)
	ln -s $(DATA_DIR)/$(OVIRT_DWH_NAME)-setup.py $(DESTDIR)$(BIN_DIR)/$(OVIRT_DWH_NAME)-setup

	# TODO
	# this should go into /var/lib or /var/run
	echo > $(DESTDIR)$(DATA_DIR)/etl/kill
