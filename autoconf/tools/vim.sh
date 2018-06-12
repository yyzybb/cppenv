#!/bin/bash

set -e

. ../lib/lib.sh

target=$PREFIX/bin/vim
pkg=vim.tar.gz
test -f $target && $target --version && exit 0

cd $TMP
download "https://github.com/vim/vim/archive/v7.4.2367.tar.gz" $pkg
tar zxf $pkg
dir=`tar tf $pkg | head -1`
cd $dir
./configure --with-features=huge --enable-multibyte \
    --enable-pythoninterp=yes --enable-rubyinterp=yes \
    --enable-luainterp=yes --enable-perlinterp=yes \
    --enable-gui=gtk2 \
    --enable-cscope \
    --with-tlib=ncurses \
    --with-python-config-dir=$PREFIX/lib/python2.7/config \
    --prefix=$PREFIX
make
make install