#!/bin/bash

set -e

. ../lib/lib.sh

prefix=$1
tmp=$2
target=$prefix/bin/g++
pkg=gcc.tar.gz
echo "main() {}" | g++ -std=c++11 -E - && exit 0 ||
test -f $target && $target --version && exit 0

cd $tmp
download "https://github.com/gcc-mirror/gcc/archive/gcc-7_1_0-release.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./contrib/download_prerequisites
mkdir gcc-build
cd gcc-build
../configure --enable-checking=release --enable-languages=c,c++ --disable-multilib --prefix=$prefix
make
