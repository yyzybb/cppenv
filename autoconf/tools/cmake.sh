#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/cmake
pkg=cmake.tar.gz
test -f $target && $target --version && exit 0

#cmake --version && exit 0

cd $TMP
download "https://github.com/Kitware/CMake/archive/v3.11.3.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./bootstrap --prefix=$PREFIX
#./configure --prefix=$PREFIX
make $MAKEFLAGS
make install
