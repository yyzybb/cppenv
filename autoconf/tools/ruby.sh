#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

target=$PREFIX/bin/ruby
pkg=ruby.tar.gz

if test -z $forceInstall
then
    test -f $target && $target --version && exit 0
fi

cd $TMP
download "https://cache.ruby-lang.org/pub/ruby/2.5/ruby-2.5.1.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --prefix=$PREFIX
make $MAKEFLAGS
make install
