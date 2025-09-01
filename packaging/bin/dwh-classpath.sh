#!/usr/bin/sh

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

if [ -z "${WILDFLYJAVACONF}" ]; then
	WILDFLYJAVACONFDIR="$(readlink -f $(dirname $(dirname $0)))/wildflyjavaconf"
fi

if [ -x /usr/bin/java-config ]; then
	PACKAGES_BUILD="dom4j-1 commons-collections jackson-core jackson-databind jackson-annotations"
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
	[ -z "${dom4j}" ] && dom4j="$(JAVACONFDIRS=${WILDFLYJAVACONFDIR} build-classpath dom4j 2> /dev/null)"
	[ -n "${dom4j}" ] || die "Cannot find dom4j"
	commons_collections="$(build-classpath apache-commons-collections 2> /dev/null)"
	[ -z "${commons_collections}" ] && commons_collections="$(build-classpath commons-collections 2> /dev/null)"
	[ -n "${commons_collections}" ] || die "Cannot find commons-collections"
	jackson_core="$(build-classpath jackson-core 2> /dev/null)"
	[ -z "${jackson_core}" ] && jackson_core="$(build-classpath jackson-core 2> /dev/null)"
	[ -n "${jackson_core}" ] || die "Cannot find jackson-core"
	jackson_databind="$(build-classpath jackson-databind 2> /dev/null)"
	[ -z "${jackson_databind}" ] && jackson_databind="$(build-classpath jackson-databind 2> /dev/null)"
	[ -n "${jackson_databind}" ] || die "Cannot find jackson-databind"
	jackson_annotations="$(build-classpath jackson-annotations 2> /dev/null)"
	[ -z "${jackson_annotations}" ] && jackson_annotations="$(build-classpath jackson-annotations 2> /dev/null)"
	[ -n "${jackson_annotations}" ] || die "Cannot find jackson-annotations"
	if [ "${what}" = "run" ]; then
		postgresql_jdbc="$(build-classpath postgresql-jdbc)" || die "Canot find postgreql-jdbc"
	fi
	output="${output}:${dom4j}:${commons_collections}:${jackson_core}:${jackson_databind}:${jackson_annotations}:${postgresql_jdbc}"
else
	die "Cannot find a method to acquire dependencies"
fi

echo "${output}"

exit 0
