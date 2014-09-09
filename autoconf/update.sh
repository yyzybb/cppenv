# Update the vim and cppenviron.
#
# * It's contains config files:
#       _vimrc
#       .ycm_extra_conf.py
#

# update newest config file
sudo git pull || exit 1

# copy _vimrc file to $HOME
cp _vimrc ~/
cp .ycm_extra_conf.py ~/

# update vim-plugins
sudo vim +BundleUpdate -c quitall

echo 'vim-env update successful, good luck!'

