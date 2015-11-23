# Install the vim and cppenviron.
# * It's contains software:
#       dos2unix
#       git
#       vim
#       g++
#       ctags
#       cmake
#       python-dev
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
sudo ./change_source_list.sh

VUNDLE_GIT=https://code.csdn.net/u014579048/vundle-vim.git
YCM_GIT=https://code.csdn.net/u014579048/youcompleteme.git
LLVM_CLANG_GIT=https://code.csdn.net/u014579048/llvm-clang.git

#VUNDLE_GIT=https://github.com/gmarik/Vundle.vim.git
#YCM_GIT=https://github.com/Valloric/YouCompleteMe.git

set -e

INSTALL_TOOL=apt-get
PY_NAME=python-dev
if [ `which apt-get 2>/dev/null | wc -l` -eq 0 ] ; then
    INSTALL_TOOL=yum
    PY_NAME=python-devel
fi
echo $INSTALL_TOOL

sudo $INSTALL_TOOL update -y

dos2unix --version || sudo $INSTALL_TOOL install dos2unix -y
dos2unix --version || exit 1

git --version || sudo $INSTALL_TOOL install git -y
git --version || exit 1

vim --version || sudo $INSTALL_TOOL install vim -y
vim --version || exit 1

g++ --version || sudo $INSTALL_TOOL install g++ -y || sudo $INSTALL_TOOL install gcc-c++ -y
g++ --version || exit 1

ctags --version || sudo $INSTALL_TOOL install ctags -y
ctags --version || exit 1

cmake --version || sudo $INSTALL_TOOL install cmake -y
cmake --version || exit 1

locate --version || sudo $INSTALL_TOOL install mlocate -y
locate --version || exit 1

sudo $INSTALL_TOOL install $PY_NAME -y

# copy _vimrc file to $HOME
dos2unix _vimrc
rm $HOME/_vimrc -f
ln _vimrc $HOME/_vimrc || cp _vimrc $HOME/_vimrc
chmod 0666 $HOME/_vimrc
dos2unix .ycm_extra_conf.py
rm $HOME/.ycm_extra_conf.py -f
cp .ycm_extra_conf.py $HOME/
chmod 0666 $HOME/.ycm_extra_conf.py

# git clone vim-vundle.git
vim_path=$HOME/.vim
vundle_path=${vim_path}/vimfiles/bundle/Vundle.vim
#echo $vim_path
#echo ${vundle_path}
while true
do
    if test -d ${vundle_path}; then
        cd ${vundle_path}
        git pull && break
    else
        git clone ${VUNDLE_GIT} ${vundle_path} && break
    fi
done

# install vim-plugins
vim +BundleInstall -c quitall

test_python_clang()
{
    echo 'import clang.cindex; s = clang.cindex.conf.lib' | python
}

install_python_clang_from_source()
{
    sudo $INSTALL_TOOL install python-clang-3.6 -y && \
    sudo $INSTALL_TOOL install libclang-3.6-dev -y || echo 'err'
}

make_llvm_clang()
{
    echo 'Not found python-clang in sys source, will install there from llvm-clang source code.'

    llvm_clang_dir=$HOME/llvm-clang
    if test -d $llvm_clang_dir; then
        cd $llvm_clang_dir
        git pull
    else
        git clone $LLVM_CLANG_GIT $llvm_clang_dir
        cd $llvm_clang_dir
    fi

    rm clang.tar llvm.tar -rf
    rm cfe-3.7.0.src llvm-3.7.0.src -rf

    xz -dk llvm.tar.xz
    xz -dk clang.tar.xz
    tar xf clang.tar
    tar xf llvm.tar

    cd llvm-3.7.0.src
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    cd ../..

    cd cfe-3.7.0.src
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    cd ..

    pyclang_dst=/usr/lib/python2.7/dist-packages
    test -d $pyclang_dst || pyclang_dst=/usr/lib/python2.7/site-packages
    sudo cp bindings/python/clang $pyclang_dst -r
    sudo echo '/usr/local/lib' > /etc/ld.so.conf.d/cppenv.conf
}

test_python_clang || install_python_clang_from_source
test_python_clang || make_llvm_clang

# compile YouCompleteMe
ycm_path=${vim_path}/vimfiles/bundle/youcompleteme
cd ${ycm_path}
./install.sh --clang-completer --system-libclang

test_python_clang || echo "Error: python-clang install error, please check libclang.so and cindex.py!"
echo 'vim-env is ok, good luck!'

