#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/ctags
pkg=ctags.tar.gz

if test -z $forceInstall
then
    test -f $target && $target --version && exit 0
fi

cd $TMP
download "http://prdownloads.sourceforge.net/ctags/ctags-5.8.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --prefix=$PREFIX
make $MAKEFLAGS
make install
