#!/bin/bash

printMsg()
{
    message "------- $1 -------"
    message "MAKEFLAGS: $MAKEFLAGS"
    message "CC: $CC"
    message "CXX: $CXX"
    message "LIBRARY_PATH: $LIBRARY_PATH"
    message "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
}

if [ $# -ge 1 ]
then
    printMsg $1
fi
