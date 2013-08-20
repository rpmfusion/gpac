#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
svn=$(date +%Y%m%d)

cd "$tmp"
svn co http://svn.code.sf.net/p/gpac/code/trunk/gpac gpac
revision=$(svnversion gpac)
echo "#define GPAC_SVN_REVISION	\"$revision\"" > gpac/include/gpac/version.h
find gpac -name ".svn" -type d  -exec rm -rf {} ';' || :
rm -rf gpac/extra_lib/
tar Jcf "$pwd"/gpac-$svn.tar.xz gpac
cd - >/dev/null
