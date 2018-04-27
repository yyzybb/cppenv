#!/bin/bash

set -e
set -x

workdir=`pwd`
cd ~
home=`pwd`
home=${home//\//\\\/}
cd -

if [ `grep export /etc/profile | wc -l` -eq 0 ]
then
    echo "Insert env"
    cp /etc/profile pf
    sed "s/\~/${home}/g" ./go_env >> pf
    sudo mv pf /etc/profile
    source /etc/profile
fi

version_large_or_equal()
{
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

install_golang()
{
    go_ver=''
    go version && go_ver=`go version | awk '{print $3}' | sed 's/\([^0-9.]\+\)//g'` || echo ''
    test ! -z $go_ver && version_large_or_equal $go_ver "1.10.1" && return 0 || echo ''
    echo "---------- download golang 1.10.1 -----------"
    cd $HOME/.vim.git
    test -f go1.10.1.linux-amd64.tar.gz || wget https://studygolang.com/dl/golang/go1.10.1.linux-amd64.tar.gz
    test -d go || tar zxf go1.10.1.linux-amd64.tar.gz
    rm $HOME/go -rf
    cp go $HOME -r
}

install_golang

cd $workdir
./goenv.sh
