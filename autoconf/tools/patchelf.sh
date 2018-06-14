#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/patchelf
pkg=patchelf.tar.gz
test -f $target && $target --version && exit 0

cd $TMP
download "https://nixos.org/releases/patchelf/patchelf-0.9/patchelf-0.9.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --prefix=$PREFIX
make $MAKEFLAGS
make install
