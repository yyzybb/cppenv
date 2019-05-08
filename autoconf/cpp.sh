#!/bin/bash

# Install:
#   cmake 3.11
#   llvm 6.0.0
#   clang 6.0.0
#   rebuild YCM
set -e

. ./lib/lib.sh $@
. ./lib/msg.sh

cd tools
./cmake.sh
./bear.sh
cd -

install_clang()
{
    clang_ver=''
    clang --version && clang_ver=`clang --version | grep version -i | awk '{print $4}' | cut -d\- -f1 | sed 's/[^0-9.]//g'` || echo -n
    test ! -z $clang_ver && version_ge $clang_ver "6.0.0" && return 0 || echo -n

    echo 'Not found clang in system, will install there from llvm-clang source code.'
    llvm_clang_dir=$TMP/llvm-clang_cppenv

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
                cd $TMP
                download http://releases.llvm.org/6.0.0/clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
                xz -dk clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
                tar xf clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04.tar
                cd clang+llvm-6.0.0-x86_64-linux-gnu-ubuntu-16.04
            else
                if [ "$os_ver" == "14.04" ]
                then
                    cd $TMP
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
        cd $TMP
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

    printMsg "build llvm"
    cd llvm-6.0.0.src
    mkdir -p build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=$HOME
    make $MAKEFLAGS
    make install
    cd ../..

    printMsg "build clang"
    cd cfe-6.0.0.src
    mkdir -p build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=$HOME
    make $MAKEFLAGS
    make install
    cd ..

    pyclang_dst=$HOME/lib/python2.7/dist-packages
    test -d $pyclang_dst || pyclang_dst=$HOME/lib/python2.7/site-packages
    test -d $pyclang_dst && cp bindings/python/clang $pyclang_dst -r
}
#install_clang

ycm_flags="--clang-completer" # --system-libclang"
if [ "$isMac" == '1' ]
then
    ycm_flags="$ycm_flags --system-libclang"
fi
which gocode && ycm_flags="$ycm_flags --go-completer"
printMsg "build YouCompleteMe flags=$ycm_flags"
ycm_path=${TMP}/YouCompleteMe
cd $ycm_path
cat ./third_party/ycmd/clang_archives/x* > ./third_party/ycmd/clang_archives/clang+llvm-5.0.0-linux-x86_64-ubuntu14.04.tar.xz
./install.py $ycm_flags

echo 'vim-cpp-env is ok, good luck!'

