#!/bin/bash

# Install:
#   cmake > 3.4.3
#   llvm = 6.0.0
#   clang = 6.0.0
#   rebuild YCM

git_clone()
{
    remote=$1
    dir=$2
    mkdir -p $dir

    cd $dir
    git status && git pull || git clone $remote .
    cd -
}

version_large_or_equal()
{
    if test -z $cmake_ver; then
        return 1
    fi

    lhs=$1
    rhs=$2
    lhs_major=`echo $lhs | cut -d. -f1`
    lhs_minor=`echo $lhs | cut -d. -f2`
    lhs_num=`echo $lhs | cut -d. -f3`
    rhs_major=`echo $rhs | cut -d. -f1`
    rhs_minor=`echo $rhs | cut -d. -f2`
    rhs_num=`echo $rhs | cut -d. -f3`
    lhs_cmp=`expr $lhs_major \* 10000 + $lhs_minor \* 100 + $lhs_num`
    rhs_cmp=`expr $rhs_major \* 10000 + $rhs_minor \* 100 + $rhs_num`
    test $lhs_cmp -ge $rhs_cmp
}

install_cmake()
{
    cmake_ver=''
    cmake --version && cmake_ver=`cmake --version | grep version -i | sed 's/\([^0-9.]\+\)//g'` || echo ''
    test ! -z $cmake_ver && version_large_or_equal $cmake_ver "3.4.3" && return 0 || echo ''

    cmake_dir=$HOME/.vim.git/cmake_cppenv
    git_clone $CMAKE_GIT $cmake_dir
    cd $cmake_dir

    tar zxf cmake.tar.gz
    ./bootstrap
    make
    sudo make install
    sudo ln -s /usr/local/bin/cmake /usr/bin/cmake || echo ''
}

install_cmake

install_clang()
{
    clang_ver=''
    clang --version && clang_ver=`cmake --version | grep version -i | sed 's/\([^0-9.]\+\)//g'` || echo ''
    test ! -z $clang_ver && version_large_or_equal $clang_ver "6.0.0" && return 0 || echo ''

    echo 'Not found clang in system, will install there from llvm-clang source code.'
    llvm_clang_dir=$HOME/.vim.git/llvm-clang_cppenv
    sudo ${workdir}/install_clang.sh $llvm_clang_dir
}
install_clang

ycm_path=${vim_path}/vimfiles/bundle/YouCompleteMe
#./install.py --clang-completer --system-libclang --go-completer
echo 'vim-cpp-env is ok, good luck!'
