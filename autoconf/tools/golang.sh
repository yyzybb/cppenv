#!/bin/bash

set -e

. ../lib/lib.sh $@
. ../lib/msg.sh $0

# check
go_ver=''

if test -z $forceInstall
then
    which go && go_ver=`go version | awk '{print $3}' | sed 's/[^0-9.]//g'` || echo -n
    test ! -z $go_ver && version_ge $go_ver "1.10.1" && exit 0 || echo -n
fi

message "---------- Download golang 1.10.1 -----------"
cd $TMP
isMac=`uname -a | grep Darwin -c || echo -n`
if [ "$isMac" == "0" ]; then
    url=https://studygolang.com/dl/golang/go1.10.1.linux-amd64.tar.gz
    pkg=go1.10.1.linux-amd64.tar.gz
else
    url=https://studygolang.com/dl/golang/go1.10.1.darwin-amd64.tar.gz
    pkg=go1.10.1.darwin-amd64.tar.gz
fi
download $url $pkg
message "---------- Uncompress package ----------"
test -d go || tar zxf $pkg
message "---------- Copy it ----------"
cp go $HOME -r || echo -n
cd -

has=`grep -c "export GOROOT=\\\$HOME/go" $PROFILE || echo -n`
if [ "$has" == "0" ]
then
    message "---------- Insert env to ~/.profile ----------"
    echo "export GOROOT=\$HOME/go" >> $PROFILE
    echo "export GOPATH=\$HOME/gopath" >> $PROFILE
    echo "export GOBIN=\$GOROOT/bin" >> $PROFILE
    echo "export PATH=\$PATH:\$GOBIN" >> $PROFILE
fi
