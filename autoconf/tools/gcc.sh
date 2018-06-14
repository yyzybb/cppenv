#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

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
make $MAKEFLAGS
make install

#set default compiler
has=`grep "export CXX=\\\$HOME/bin/g++" -c $PROFILE || echo -n`
if [ "$has" == "0" ]
then
    echo "export CC=\$HOME/bin/gcc" >> $PROFILE
    echo "export CXX=\$HOME/bin/g++" >> $PROFILE
    echo "export LIBRARY_PATH=\$HOME/lib:\$HOME/lib64:\$HOME/lib/gcc/x86_64-pc-linux-gnu/:\$LIBRARY_PATH" >> $PROFILE
    echo "export LD_LIBRARY_PATH=\$HOME/lib:\$HOME/lib64:\$HOME/lib/gcc/x86_64-pc-linux-gnu/:\$LD_LIBRARY_PATH" >> $PROFILE
fi
