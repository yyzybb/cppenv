#!/bin/sh

user_name="test"

sudo cp ./git_cmd/* /usr/local/bin

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

