# change apt-get sources.list

os_ver=`cat /etc/os-release | grep VERSION_ID | cut -d\" -f2`
os_name=`cat /etc/os-release | grep NAME | head -n1 | cut -d\" -f2`

echo "Current OS: " $os_name
echo "Version: " $os_ver

if [ $os_name != 'Ubuntu' ] ; then
    echo 'Only used to Ubuntu System.'
    exit 1
fi

if ! test -f sources/${os_name}${os_ver}; then
    echo 'sources file is not exist!'
    exit 2
fi

if test -f '/etc/apt/sources.list'; then
    if ! test -d '/etc/apt/sources.list.bak'; then
        mkdir /etc/apt/sources.list.bak
    fi
fi

cp /etc/apt/sources.list /etc/apt/sources.list.bak/sources.list.bak_`date +%Y-%m-%d_%H-%M-%S`
cat sources/Ubuntu14.04 > /etc/apt/sources.list
echo 'Change sources.list OK!'
