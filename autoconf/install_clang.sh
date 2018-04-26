#!/bin/sh

set -e

PATH=$PATH:/usr/local/bin

git_clone()
{
    remote=$1
    dir=$2
    mkdir -p $dir

    cd $dir
    git status && git pull || git clone $remote .
    cd -
}

llvm_clang_dir=$1
LLVM_CLANG_GIT=https://gitee.com/yyzybb537/llvm-clang.git
git_clone $LLVM_CLANG_GIT $llvm_clang_dir
cd $llvm_clang_dir

xz -dk llvm.tar.xz || echo ''
xz -dk clang.tar.xz || echo ''
tar xf clang.tar
tar xf llvm.tar

cd llvm-6.0.0.src
mkdir -p build
cd build
cmake ..
make
sudo make install
cd ../..

cd cfe-6.0.0.src
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
