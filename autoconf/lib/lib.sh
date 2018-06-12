#!/bin/bash

set -x

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

git_clone()
{
    remote=$1
    dir=$2
    mkdir -p $dir

    cd $dir
    git status && git pull || git clone $remote .
    cd -
}
