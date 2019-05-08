#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/bear

if test -z $forceInstall
then
    test -f $target && $target --version && exit 0
fi

cd $TMP
downloadByGit "https://github.com/rizsotto/Bear.git" Bear
cd Bear
mkdir build -p
cd build/
cmake .. -DCMAKE_INSTALL_PREFIX=$PREFIX
make $MAKEFLAGS
make install
