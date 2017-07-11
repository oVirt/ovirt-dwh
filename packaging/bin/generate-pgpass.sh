#!/bin/sh

. "$(dirname "$(readlink -f "$0")")"/dwh-prolog.sh

[[ -z $DWH_DB_HOST ]]     || \
[[ -z $DWH_DB_PORT ]]     || \
[[ -z $DWH_DB_USER ]]     || \
[[ -z $DWH_DB_DATABASE ]] && die "Can't parse the connection details"

MYTEMP="$(mktemp -d)"

generatePgPass() {
	local password="$(echo "${DWH_DB_PASSWORD}" | sed -e 's/\\/\\\\/g' -e 's/:/\\:/g')"
	export PGPASSFILE="${MYTEMP}/.pgpass"
	touch "${PGPASSFILE}" || die "Can't create ${PGPASSFILE}"
	chmod 0600 "${PGPASSFILE}" || die "Can't chmod ${PGPASSFILE}"

	cat > "${PGPASSFILE}" << __EOF__
${DWH_DB_HOST}:${DWH_DB_PORT}:${DWH_DB_DATABASE}:${DWH_DB_USER}:${password}
__EOF__
}

cleanup() {
	[ -n "${MYTEMP}" ] && rm -fr "${MYTEMP}" ]
}
trap cleanup 0
