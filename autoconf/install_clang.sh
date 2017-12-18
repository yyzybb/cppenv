#!/bin/sh

set -e

PATH=$PATH:/usr/local/bin

llvm_clang_dir=$1
LLVM_CLANG_GIT=https://gitee.com/yyzybb537/llvm-clang.git
if test -d $llvm_clang_dir; then
    cd $llvm_clang_dir
    git pull
else
    git clone $LLVM_CLANG_GIT $llvm_clang_dir
    cd $llvm_clang_dir
fi

xz -dk llvm.tar.xz || echo ''
xz -dk clang.tar.xz || echo ''
tar xf clang.tar
tar xf llvm.tar

cd llvm-3.7.0.src
mkdir -p build
cd build
cmake ..
make
sudo make install
cd ../..

cd cfe-3.7.0.src
mkdir -p build
cd build
cmake ..
make
sudo make install
cd ..

pyclang_dst=/usr/lib/python2.7/dist-packages
test -d $pyclang_dst || pyclang_dst=/usr/lib/python2.7/site-packages
cp bindings/python/clang $pyclang_dst -r
echo '/usr/local/lib' > /etc/ld.so.conf.d/cppenv.conf
