#!/bin/bash

set -e

. ../lib/lib.sh

target=$PREFIX/bin/g++
pkg=gcc.tar.gz
echo "main() {}" | g++ -std=c++11 -E - && exit 0 ||
test -f $target && $target --version && exit 0

cd $TMP
download "https://github.com/gcc-mirror/gcc/archive/gcc-7_1_0-release.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./contrib/download_prerequisites
mkdir gcc-build
cd gcc-build
../configure --enable-checking=release --enable-languages=c,c++ --disable-multilib --prefix=$PREFIX
make
make install

#set default compiler
has=`grep "export CXX" -c $HOME/.profile || echo -n`
if [ "$has" == "0" ]
then
    echo "export CC=$HOME/bin/gcc" >> $HOME/.profile
    echo "export CXX=$HOME/bin/g++" >> $HOME/.profile
fi
