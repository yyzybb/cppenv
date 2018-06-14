#!/bin/bash

. ./lib/lib.sh $@

cd tools
./golang.sh
source $PROFILE

set +e
go get -v github.com/yyzybb537/goinstall
go get -v github.com/kardianos/govendor
go get -v github.com/rogpeppe/godef
go get -v github.com/bradfitz/goimports
go get -v github.com/bytbox/golint
go get -v github.com/jstemmer/gotags
go get -v github.com/kisielk/errcheck
go get -v github.com/golang/tools

set -e
go get -v github.com/nsf/gocode

cd ${VIMPATH}/vimfiles/bundle/YouCompleteMe
./install.py --go-completer
