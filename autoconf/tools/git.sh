#!/bin/bash

set -e

. ../lib/lib.sh

prefix=$1
tmp=$2
target=$prefix/bin/git
pkg=git.tar.gz
test -f $target && $target --version && exit 0

#git --version && exit 0
cd $tmp
download "https://www.kernel.org/pub/software/scm/git/git-2.12.2.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --prefix=$prefix
make
make install
