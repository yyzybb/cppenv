#!/bin/bash

. ./lib/lib.sh $@

# patchelf
patch_rpath()
{
    patchelf --set-rpath $HOME/lib:$HOME/lib64:$HOME/gcc/x86_64-pc-linux-gnu $1
}
for elf in `ls $HOME/bin`
do
    patch_rpath $HOME/bin/$elf || echo "patchelf $HOME/bin/$elf error."
done

patchelf --set-rpath \
    $VIMPATH/vimfiles/bundle/YouCompleteMe/third_party/ycmd:$HOME/lib:$HOME/lib64:$HOME/gcc/x86_64-pc-linux-gnu \
    $VIMPATH/vimfiles/bundle/YouCompleteMe/third_party/ycmd/ycm_core.so
