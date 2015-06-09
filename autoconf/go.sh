#!/bin/sh -x

sudo cat ./go_env >> /etc/profile
source /etc/profile

DIR=/usr/local/go/src/golang.org/x
mkdir -p $DIR
cd $DIR
test ! -d tools && git clone https://github.com/golang/tools.git

cd $DIR/tools/cmd/gorename && go build && go install
cd $DIR/tools/cmd/oracle && go build && go install

go get github.com/nsf/gocode
go get github.com/rogpeppe/godef 
go get github.com/bradfitz/goimports
go get github.com/bytbox/golint
go get github.com/jstemmer/gotags
go get github.com/kisielk/errcheck

