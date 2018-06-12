#!/bin/bash

set -e

. ../lib/lib.sh

pkg=ncurses.tar.gz
test -d $PREFIX/include/ncurses && exit 0

cd $TMP
download "http://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --prefix=$PREFIX
make
make install
