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

#cd ~
#if test ! -d go
#then 
#    git clone https://git.oschina.net/yyzybb537/go.git
#else
#    cd go
#    git pull
#    cd ~
#fi
#
#if [ `which go | wc -l` -eq 0 ]
#then
#    cp go go1.4 -r
#    cd go1.4/src
#    git checkout release-branch.go1.4
#    ./all.bash
#    cd -
#    cd go/src
#    git checkout release-branch.go1.7
#    ./all.bash
#    cd -
#fi

cd $workdir
./goenv.sh
