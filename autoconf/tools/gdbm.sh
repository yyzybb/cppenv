#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/gdbmtool
pkg=gdbm-1.18.1.tar.gz

if test -z $forceInstall
then
    test -f $target && $target --version && exit 0
fi

cd $TMP
download "ftp://ftp.gnu.org/gnu/gdbm/gdbm-1.18.1.tar.gz" $pkg
tar zxf $pkg
dir=gdbm-1.18.1
cd $dir
./configure --prefix=$PREFIX
make $MAKEFLAGS
make install
