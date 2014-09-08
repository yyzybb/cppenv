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

# install dos2unix, git, vim, g++, ctags, cmake, python-dev
sudo apt-get update -y || exit 1

dos2unix --version || sudo apt-get install dos2unix -y
dos2unix --version || exit 1

git --version || sudo apt-get install git -y
git --version || exit 1
git config --global user.email user_email@gmail.com
git config --global user.name user_name

vim --version || sudo apt-get install vim -y
vim --version || exit 1

g++ --version || sudo apt-get install g++ -y
g++ --version || exit 1

ctags --version || sudo apt-get install ctags -y
ctags --version || exit 1

cmake --version || sudo apt-get install cmake -y
cmake --version || exit 1

sudo apt-get install python-dev -y

# copy _vimrc file to $HOME
dos2unix _vimrc
cp _vimrc ~/
dos2unix .ycm_extra_conf.py
cp .ycm_extra_conf.py ~/

# git clone vim-vundle.git
vim_path=`vim --version | grep '$VIM:' | cut -d'"' -f2`
vundle_path=${vim_path}/vimfiles/bundle/Vundle.vim
#echo $vim_path
#echo ${vundle_path}
if test -d ${vundle_path}; then
    cd ${vundle_path}
    sudo git pull || exit 2
else
    sudo git clone https://github.com/gmarik/Vundle.vim.git ${vundle_path} || exit 2
fi

# install vim-plugins
sudo vim +BundleInstall -c quitall

# compile YouCompleteMe
cd ${vim_path}/vimfiles/bundle/YouCompleteMe
sudo git submodule update --init --recursive
sudo ./install.sh --clang-completer || exit 3


