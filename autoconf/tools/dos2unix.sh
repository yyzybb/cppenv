#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/dos2unix
pkg=dos2unix-dos2unix-861184d55fd86da787c4e16855461b3b8f40b4b0.zip

if test -z $forceInstall
then
    dos2unix --version && exit 0
    test -f $target && $target --version && exit 0
fi

cd $TMP
download "https://sourceforge.net/code-snapshots/git/d/do/dos2unix/dos2unix.git/dos2unix-dos2unix-861184d55fd86da787c4e16855461b3b8f40b4b0.zip" $pkg
unzip $pkg
dir=dos2unix-dos2unix-861184d55fd86da787c4e16855461b3b8f40b4b0
cd $dir
make || true
cp dos2unix $target
test -f $target && $target --version
