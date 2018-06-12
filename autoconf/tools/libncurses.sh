#!/bin/bash

set -e

. ../lib/lib.sh

prefix=$1
tmp=$2
pkg=ncurses.tar.gz
test -d $prefix/include/ncurses && exit 0

cd $tmp
download "http://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --prefix=$prefix
make
make install
