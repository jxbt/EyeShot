#!/bin/bash

if [ $(id -u) = "0" ];

then

    apt-get update

    apt-get install firefox
    pip3 install selenium

    wsinstall_Path="/usr/bin/eyeshot"
    firefox_binPath=$(which firefox)

    cp eyeshot.py $wsinstall_Path
    sed -i 's|binPath|'$firefox_binPath'|g' $wsinstall_Path
    chmod +x $wsinstall_Path

    printf "\n\n\ninstallation Done! \n"

else

    printf "you should run the installation file as root using the sudo command:\n\n"
    printf "sudo $0\n\n"

fi
