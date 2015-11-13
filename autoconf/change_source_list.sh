# change apt-get sources.list
set -e

os_ver=`cat /etc/os-release | grep VERSION_ID | cut -d\" -f2`
os_name=`cat /etc/os-release | grep NAME | head -n1 | cut -d\" -f2`

echo "Current OS: " $os_name
echo "Version: " $os_ver

# yum
if test -f /etc/centos-release ; then
    if [ "$os_ver" == '7' ] ; then
        test -f /etc/yum.repos.d/CentOS-Base.repo && sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak_`date +%Y-%m-%d_%H-%M-%S`
        sudo cp sources/CentOS7-Base-163.repo /etc/yum.repos.d
	echo 'Change sources.list OK!'
        exit 0
    fi

    echo 'Not support System.'
    exit 1
fi

# apt-get
if ! test -f "sources/${os_name}${os_ver}"; then
    echo 'sources file is not exist!'
    exit 2
fi

if test -f '/etc/apt/sources.list'; then
    if ! test -d '/etc/apt/sources.list.bak'; then
        mkdir /etc/apt/sources.list.bak
    fi
fi

cp /etc/apt/sources.list /etc/apt/sources.list.bak/sources.list.bak_`date +%Y-%m-%d_%H-%M-%S`
cat sources/${os_name}${os_ver} > /etc/apt/sources.list
echo 'Change sources.list OK!'

