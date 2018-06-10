#!/bin/sh

#
# execute site local script if available
#
if [ -x "$0.local" ]; then
	exec "$0.local"
	exit 1
fi

die() {
	local m="$1"
	echo "FATAL: ${m}" >&2
	exit 1
}

what="$1"
output=""

case "${what}" in
	build|run);;
	*) die "Invalid usage";;
esac

if [ -z "${JAVA_HOME}" ]; then
	JAVA_HOME="$(/usr/share/ovirt-engine/bin/java-home)"
	export JAVA_HOME
fi

if [ -x /usr/bin/java-config ]; then
	PACKAGES_BUILD="dom4j-1 commons-collections"
	PACKAGES_RUNTIME="jdbc-postgresql"

	packages="${PACKAGES_BUILD}"
	args=
	if [ "${what}" = "run" ]; then
		packages="${packages} ${PACKAGES_RUNTIME}"
		args="${args} -d"
	fi
	for package in ${packages}; do
		output="${output}:$(java-config ${args} -p ${package} 2> /dev/null)" \
			|| die "Cannot locate ${package}"
	done
elif [ -x /usr/bin/build-classpath ]; then
	dom4j="$(build-classpath dom4j 2> /dev/null)"
	[ -z "${dom4j}" ] && dom4j="$(build-classpath dom4j-eap6 2> /dev/null)"
	[ -n "${dom4j}" ] || die "Cannot find dom4j"
	commons_collections="$(build-classpath apache-commons-collections 2> /dev/null)"
	[ -z "${commons_collections}" ] && commons_collections="$(build-classpath commons-collections 2> /dev/null)"
	[ -n "${commons_collections}" ] || die "Cannot find commons-collections"
	if [ "${what}" = "run" ]; then
		postgresql_jdbc="$(build-classpath postgresql-jdbc)" || die "Canot find postgreql-jdbc"
	fi
	output="${output}:${dom4j}:${commons_collections}:${postgresql_jdbc}"
else
	die "Cannot find a method to acquire dependencies"
fi

echo "${output}"

exit 0
