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
svn export http://gpac.svn.sourceforge.net/svnroot/gpac/trunk/gpac gpac
rm -rf gpac/extra_lib/
tar jcf "$pwd"/gpac-$svn.tar.bz2 gpac
cd - >/dev/null
