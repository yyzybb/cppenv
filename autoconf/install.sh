# Install the vim and cppenviron.
# * It's contains software:
#       git
#       vim
#       g++
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

# install git, vim, g++
git --version || sudo apt-get install git
git --version || echo 'install git fail.' && exit 1
git config --global user.email user_email@gmail.com
git config --global user.name user_name

vim --version || sudo apt-get install vim
vim --version || echo 'install vim fail.' && exit 1

g++ --version || sudo apt-get install g++
g++ --version || echo 'install g++ fail.' && exit 1

# copy _vimrc file to $HOME
cp _vimrc ~
cp .ycm_extra_conf.py ~

# git clone vim-vundle.git
vim_path=`vim --version | grep '$VIM:' | cut -d'"' -f2`
vundle_path=${vim_path}/vimfiles/bundle/Vundle.vim
#echo $vim_path
#echo ${vundle_path}
if test -d ${vundle_path}; then
    cd ${vundle_path}
    git pull || echo 'git pull Vundle fail.' && exit 2
else
    git clone https://github.com/gmarik/Vundle.vim.git ${vundle_path} || echo 'git clone Vundle fail.' && exit 2
fi

# install vim-plugins
vim +BundleInstall

# compile YouCompleteMe
cd ${vim_path}/vimfiles/bundle/YouCompleteMe
git submodule update --init --recursive
./install.sh --clang-completer || echo 'install YouCompleteMe fail.' && exit 3


