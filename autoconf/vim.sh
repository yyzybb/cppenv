#!/bin/bash

# Install the vim and cppenviron.
#
# * Need tools:
#       wget
#       dos2unix
#
# * It's contains software:
#       git
#       g++ supports -std=c++11
#       vim 7.4.2367
#       ctags
#       python
#       python-dev
#       ruby
#       ruby-dev
#
# * Vim plugins:
#       vim-YouCompleteMe
#       vim-vundle
#       vim-airline
#       vim-nerdtree
#       vim-taglist
#       vim-cppenv.
#
# * And contains config files:
#       _vimrc
#       .ycm_extra_conf.py
#

# install dos2unix, git, vim, g++, ctags, cmake, python-dev

. ./lib/lib.sh $@
. ./lib/msg.sh

set -e

workdir=`pwd`
if [ "$isMac" == '1' ]
then
    brew --version || /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew update
    wget --version || brew install wget
    dos2unix --version || brew install dos2unix
    echo 'MacOS brew installed OK'
fi

# config git address
VUNDLE_GIT=https://gitee.com/yyzybb537/Vundle.vim.git
YCM_GIT=https://gitee.com/yyzybb537/YouCompleteMe.git

# update profile
has=`grep "export PATH=\\\$HOME/bin:\\\$PATH" -c $PROFILE || echo -n`
if [ "$has" == "0" ]
then
    echo "export PATH=\$HOME/bin:\$PATH" >> $PROFILE
fi

# install tools
cd tools
./gcc.sh
source $PROFILE
./git.sh
./ctags.sh
./patchelf.sh
#./mlocate.sh

if [ "$isMac" == "0" ]; then
    ./libncurses.sh
    ./python.sh
    ./ruby.sh
    ./vim.sh
fi
cd -

# init git config, copy git_cmd and shell_cmd to BIN
cp git_cmd/* $BIN
cp shell_cmd/* $BIN
user_name=`whoami`
if [ `git config --global --list | grep user | wc -l` -eq 0 ]
then
    git config --global user.email $user_name@gmail.com
    git config --global user.name $user_name
fi
git config --global diff.tool vimdiff
git config --global diff.prompt false
git config --global merge.tool vimdiff
git config --global merge.prompt false
git config --global alias.br "branch -av"
git config --global alias.ss status
git config --global alias.co checkout
git config --global alias.cmt commit
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.lgf "log --name-status"
git config --global receive.denyCurrentBranch true
git config --global core.editor vim

# copy _vimrc and .ycm_extra_conf to $HOME
dos2unix _vimrc
rm $HOME/_vimrc -f
ln _vimrc $HOME/_vimrc || cp _vimrc $HOME/_vimrc
chmod 0666 $HOME/_vimrc
dos2unix .ycm_extra_conf.py
rm $HOME/.ycm_extra_conf.py -f
cp .ycm_extra_conf.py $HOME/
chmod 0666 $HOME/.ycm_extra_conf.py
vim_exe=`which vim`
vim_exe_dir=`dirname $vim_exe`
mkdir -p $HOME/bin
rm $HOME/bin/v -f
ln -s ${vim_exe_dir}/vim $HOME/bin/v || echo -n

# git clone vim-vundle.git
vundle_path=${VIMPATH}/vimfiles/bundle/Vundle.vim
git_clone ${VUNDLE_GIT} ${vundle_path}

# compile YouCompleteMe
printMsg "build YouCompleteMe --go-completer"
ycm_path=${VIMPATH}/vimfiles/bundle
ycm_path_ori=${TMP}/YouCompleteMe
git_clone ${YCM_GIT} ${ycm_path_ori}
ln -s ${ycm_path_ori} ${ycm_path} || echo -n
#cd ${ycm_path}
#./install.py

# install other's vim-plugins
vim +BundleInstall -c quitall

echo 'vim-base-env is ok, good luck!'

