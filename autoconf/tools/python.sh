#!/bin/bash

set -e

. ../lib/lib.sh

target=$PREFIX/bin/python
pkg=python.tar.xz
test -f $target && $target --version && exit 0

cd $TMP
download "https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz" $pkg
xz -dk $pkg
tar xf python.tar
dir=`tar tf python.tar | head -1`
cd $dir
./configure --prefix=$PREFIX
./configure --prefix=$PREFIX --enable-shared LDFLAGS="-Wl,-rpath $PREFIX/lib" --enable-unicode=ucs4 
make
make install
make commoninstall
