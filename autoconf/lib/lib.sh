#!/bin/bash

set -e

export PREFIX=$HOME
export VIMPATH=$HOME/.vim
export TMP=$HOME/.vim.git
export PROFILE=$HOME/.profile
export BIN=$HOME/bin
export isMac=`uname -a | grep Darwin -c || echo -n`
export forceInstall=
export withGo=0

mkdir -p $TMP
mkdir -p $VIMPATH
mkdir -p $BIN
test ! -f $PROFILE && touch $PROFILE || echo -n

message() {
    echo -e "\033[32m$@\033[0m"
}

error() {
    echo -e "\033[31m$@\033[0m"
}

download() {
    url=$1
    filename=$2
    has=`md5sum -c ${filename}.md5 2>/dev/null >/dev/null && echo 1 || echo 0`
    if [ "$has" == "0" ]
    then
        message "----> Download $filename"
        wget $url -O $filename && md5sum $filename > ${filename}.md5
        message "====> Download $filename Success"
    else
        message "====> Exists $filename"
    fi
}

downloadByGit() {
    url=$1
    dir=$2
    if test -d $dir
    then
        message "----> git pull $url"
        cd $dir && git pull
        cd ..
    else
        message "----> git clone $url"
        git clone $url $dir
    fi
}

git_clone()
{
    remote=$1
    dir=$2
    mkdir -p $dir

    cd $dir
    git status && git pull || git clone $remote .
    cd -
}

usage()
{
    message "Flags: (-j4|-j8|...)"
}

while getopts "j:h:f:g" optvar
do
    case $optvar in
        j):
            __makeflags="-j$OPTARG"
            ;;
        f):
            export forceInstall=1
            ;;
        g):
            export withGo=1
            ;;
        h):
            usage
            exit 1
            ;;
    esac
done

if [ "$CPPENV_LIB_SHELL_INITED" == "" -o "$__makeflags" != "" ]
then
    export CPPENV_LIB_SHELL_INITED=1
    export MAKEFLAGS=$__makeflags
    message "set MAKEFLAGS=$MAKEFLAGS"
fi

version_ge()
{
    lhs=$1
    rhs=$2
    lhs_major=`echo $lhs | cut -d. -f1`
    lhs_minor=`echo $lhs | cut -d. -f2`
    lhs_num=`echo $lhs | cut -d. -f3`
    test -z $lhs_major && lhs_major=0 || echo -n
    test -z $lhs_minor && lhs_minor=0 || echo -n
    test -z $lhs_num && lhs_num=0 || echo -n

    rhs_major=`echo $rhs | cut -d. -f1`
    rhs_minor=`echo $rhs | cut -d. -f2`
    rhs_num=`echo $rhs | cut -d. -f3`
    test -z $rhs_major && rhs_major=0 || echo -n
    test -z $rhs_minor && rhs_minor=0 || echo -n
    test -z $rhs_num && rhs_num=0 || echo -n

    lhs_cmp=`expr $lhs_major \* 10000 + $lhs_minor \* 100 + $lhs_num`
    rhs_cmp=`expr $rhs_major \* 10000 + $rhs_minor \* 100 + $rhs_num`
    test $lhs_cmp -ge $rhs_cmp
}

