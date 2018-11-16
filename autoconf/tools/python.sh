#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/python
pkg=python.tar.xz

if test -z $forceInstall
then
    test -f $target && $target --version && exit 0
    echo 'import dbm' | python - && exit 0
fi

./gdbm.sh

cd $TMP
download "https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz" $pkg
xz -dkf $pkg
tar xf python.tar
dir=`tar tf python.tar | head -1`
cd $dir
./configure --prefix=$PREFIX
./configure --prefix=$PREFIX --enable-shared LDFLAGS="-Wl,-rpath $PREFIX/lib" --enable-unicode=ucs4 
make $MAKEFLAGS
make install
make commoninstall
