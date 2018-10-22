#!/bin/bash

banner(){

clear

echo "
  _______         _          _       _
 |__   __|       | |        | |     (_)
    | |     ___  | |   ___  | |__    _  __  __
    | |    / _ \ | |  / _ \ | '_ \  | | \ \/ /
    | |   |  __/ | | |  __/ | |_) | | |  >  <
    |_|    \___| |_|  \___| |_.__/  |_| /_/\_\\

"
echo "[+] How to use: sudo ./setup.sh --install | --uninstall"

}


howtouse(){
	echo "[+] How to use: sudo ./setup.sh --install | --uninstall"
}

install(){

	banner
	if [ "$(id -u)" != "0" ]; then

	echo "[+] This script must be run as root" 1>&2
		exit 1
	fi
	apt-get update
	apt-get install -y python-pip
	apt-get install -y python-qt4
	apt-get install -y python-dev git
	pip install -r requirements.txt
	echo "[+] Checking old installations..."
	if [ -d "$path" ]; then
		rm -r $path
	echo "[+] Old installations removed!"
	fi
	mkdir $path
	cp -r $path_packages /usr/share/telebix/
    if which update-alternatives >/dev/null; then
        update-alternatives --install /usr/bin/telebix telebix /usr/share/telebix/telebix 1 > /dev/null
    else
        ln -sfT /usr/share/telebix/telebix /usr/bin/telebix
    fi
    cp telebix.desktop /usr/share/applications/telebix.desktop
    chmod +x /usr/share/telebix/telebix
	echo "[+] Telebix installed successfully!"
	exit 0
}

uninstall(){
	if [ "$(id -u)" != "0" ]; then
		echo "[+] This script must be run as root" 1>&2
		exit 1
	fi
	if [  -d "$path" ]; then
            if which update-alternatives >/dev/null; then
                update-alternatives --remove telebix /usr/share/telebix > /dev/null
            else
                rm /usr/bin/telebix
            fi
            rm /usr/share/applications/telebix.desktop
	    	rm -r $path"/"
	    	echo "[+] Telebix uninstalled successfully!"
	else
	    echo "[+] Telebix is not installed!"
	fi
}

banner
path="/usr/share/telebix"
path_packages=$(pwd)"/*"

while [ "$1" != "" ]; do
    case $1 in
        --install ) install
        ;;
        --uninstall ) uninstall
        ;;
        * ) howtouse
 
       exit 1
    esac
    shift
done
