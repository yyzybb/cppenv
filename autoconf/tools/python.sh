#!/bin/bash

set -e

. ../lib/lib.sh

prefix=$1
tmp=$2
target=$prefix/bin/python
pkg=python.tar.xz
test -f $target && $target --version && exit 0

cd $tmp
download "https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz" $pkg
cp $pkg ${pkg}.back
xz -d $pkg
mv ${pkg}.back $pkg
tar xf python.tar
dir=`tar tf python.tar | head -1`
cd $dir
./configure --prefix=$prefix
./configure --prefix=$prefix --enable-shared LDFLAGS="-Wl,-rpath $prefix/lib" --enable-unicode=ucs4 
make
make install
make commoninstall
