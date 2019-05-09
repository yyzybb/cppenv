#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/dos2unix
pkg=dos2unix.tar.gz

if test -z $forceInstall
then
    dos2unix --version && exit 0
    test -f $target && $target --version && exit 0
fi

cd $TMP
downloadByGit "https://gitee.com/yyzybb537/vim-tgz.git" vimgit
cd vimgit
tar zxf $pkg
dir=dos2unix
cd $dir
make || true
sleep 1
cp dos2unix $target
test -f $target && $target --version
