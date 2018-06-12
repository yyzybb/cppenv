#!/bin/bash

# Install:
#   cmake 3.11
#   llvm 6.0.0
#   clang 6.0.0
#   rebuild YCM
set -e

. ./lib/lib.sh
cd tools
./cmake.sh
cd -

install_clang()
{
    clang_ver=''
    clang --version && clang_ver=`clang --version | grep version -i | sed 's/[^0-9.]//g'` || echo -n
    test ! -z $clang_ver && version_large_or_equal $clang_ver "6.0.0" && return 0 || echo -n

    echo 'Not found clang in system, will install there from llvm-clang source code.'
    mkdir -p $HOME/.vim.git
    llvm_clang_dir=$HOME/.vim.git/llvm-clang_cppenv

    built_from_source=0

    isMac=`uname -a | grep Darwin -c || echo -n`
    echo "isMac:" $isMac
    if [ "$isMac" == "0" ]; then
        os_ver=`cat /etc/os-release | grep VERSION_ID | cut -d\" -f2`
        os_name=`cat /etc/os-release | grep NAME | head -n1 | cut -d\" -f2`
        echo "Current OS: " $os_name
        echo "Version: " $os_ver

        if [ "$os_name" == "Ubuntu" ]
        then
            if [ "$os_ver" == "16.04" ]
            then
                cd $HOME/.vim.git
                download http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
                xz -dk clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
                tar xf clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar
                cd clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04
            else
                if [ "$os_ver" == "14.04" ]
                then
                    cd $HOME/.vim.git
                    download http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz
                    xz -dk clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz
                    tar xf clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-14.04.tar
                    cd clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-14.04
                else
                    built_from_source=1
                fi
            fi
        fi
    else
        echo "download clang6.0-Darwin"
        cd $HOME/.vim.git
        download http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz
        xz -dk clang+llvm-6.0.0-x86_64-apple-darwin.tar.xz
        tar xf clang+llvm-6.0.0-x86_64-apple-darwin.tar
        cd clang+llvm-6.0.0-x86_64-apple-darwin
        exit 0
    fi

    if [ "$built_from_source" == "0" ]
    then
        cp include/* $HOME/include -r
        cp lib/* $HOME/lib -r
        cp libexec/* $HOME/bin
        cp bin/* $HOME/bin
        return
    fi

    LLVM_CLANG_GIT=https://gitee.com/yyzybb537/llvm-clang.git
    git_clone $LLVM_CLANG_GIT $llvm_clang_dir
    cd $llvm_clang_dir

    xz -dk llvm.tar.xz || echo -n
    xz -dk clang.tar.xz || echo -n
    tar xf clang.tar
    tar xf llvm.tar

    cd llvm-6.0.0.src
    mkdir -p build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=$HOME
    make
    make install
    cd ../..

    cd cfe-6.0.0.src
    mkdir -p build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=$HOME
    make
    make install
    cd ..

    pyclang_dst=$HOME/lib/python2.7/dist-packages
    test -d $pyclang_dst || pyclang_dst=$HOME/lib/python2.7/site-packages
    test -d $pyclang_dst && cp bindings/python/clang $pyclang_dst -r
}
install_clang

ycm_path=$HOME/.vim/vimfiles/bundle/YouCompleteMe
cd $ycm_path
./install.py --clang-completer --system-libclang --go-completer
echo 'vim-cpp-env is ok, good luck!'

