#!/bin/sh

cd $(git rev-parse --show-toplevel)

# Check for copyright notices in files that do not also include an SPDX tag.
non_removed_files=$( \
	git show --pretty="format:" --name-status | \
	awk '/^[^D]/ {print $2}' \
)

copyright_notices_files=
[ -n "${non_removed_files}" ] && copyright_notices_files=$( \
	echo "${non_removed_files}" | \
	xargs grep -il 'Copyright.*Red Hat' \
) || true

copyright_notices_no_spdx_files=
[ -n "${copyright_notices_files}" ] && copyright_notices_no_spdx_files=$( \
	echo "${copyright_notices_files}" | \
	xargs grep -iL 'SPDX' \
) || true

if [ -n "${copyright_notices_no_spdx_files}" ]; then
	cat << __EOF__
[ERROR] : The following file(s) contain copyright/license notices, and do not contain an SPDX tag:
============================================================
${copyright_notices_no_spdx_files}
============================================================
Please replace the notices with an SPDX tag. How exactly to do this is language/syntax specific. You should include the following two lines in a comment:
============================================================
Copyright oVirt Authors
SPDX-License-Identifier: Apache-2.0
============================================================
__EOF__
	exit 1
fi
