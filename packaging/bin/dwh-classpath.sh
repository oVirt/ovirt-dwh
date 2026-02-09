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

if [ -x /usr/bin/build-classpath ]; then
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
	output="${output}:${dom4j}:${commons_collections}:${jackson_core}:${jackson_databind}:${jackson_annotations}"
	if [ "${what}" = "run" ]; then
		postgresql_jdbc="$(build-classpath postgresql-jdbc)" || die "Cannot find postgreql-jdbc"
		output="${output}:${postgresql_jdbc}"
		ongres_scram="$(build-classpath ongres-scram)"
		[ -n "${ongres_scram}" ] && output="${output}:${ongres_scram}"
		ongres_stringprep="$(build-classpath ongres-stringprep)"
		[ -n "${ongres_stringprep}" ] && output="${output}:${ongres_stringprep}"
	fi
else
	die "Cannot find a method to acquire dependencies"
fi

echo "${output}"

exit 0
