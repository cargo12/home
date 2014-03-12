#!/bin/bash
# $Id: padlock  06-26-2008 09:44AM v.08.178.0944 wimac Exp $
# Modification-Date: Sun 21 Nov 2010 13:36:55 -0500
# Written by: William J. MacLeod (wimac1@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of #the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Locks directories and files
FILES="
/home/$USER/.p
"
PROG=${0##*/}
VERSION=$(echo $Revision: 1.6 $ |awk '{print$2}')
ENCPW="NDBsZGZhNVQjdHJwdCFyM2RkMGcK"
PW=$(echo "$ENCPW" | base64 --decode)
killshit()
{
    fuser -kms /media/wimac-drive
}

usage()
{  echo "This script locks directories."
   echo "Usage: $PROG [OPTIONS]"
   echo '  No Options locks directories'
   echo '  Options:'
   echo '     u  | -u | --unlock    unlocks directories'
   echo '    -h, --help      displays this message'
   echo '    -V, --version   display program version and author info'
   echo 
}

tdrive()
{
        if [ -f /media/wimac-drive02/data.p ]; then
             $1 /media/wimac-drive
             $1 /media/wimac-drive02
         fi
    }

plock() { 
    if [ -d .p ]; then
        echo $PW > /tmp/pwf
        #tar czf /tmp/dat.tgz .p | gpg --cipher-algo aes256 -c --passphrase-file /tmp/pwf -o - > ~/Dropbox/dat.enc
        tar czf /tmp/dat.tgz .p
        openssl enc -aes-256-cbc -salt -in /tmp/dat.tgz -out ~/Dropbox/dat.enc -pass file:/tmp/pwf  
        srm /tmp/dat.tgz /tmp/pwf
        rm -R .p
        rm lpriv 
       
    fi
#        killshit
    if [ -f /dev/mapper/truecrypt1 ]; then
        fuser -kms /dev/mapper/truecrypt1
        
    fi

            truecrypt -t -d --force &
            sleep 3
            echo "" 
            echo -e "--[ \e[1;31m click \e[0m ]--"
            echo ""
       # umount
          }
ulock() {
        echo "" 
        if [ -f /media/wimac-drive02/data.p ] 
      then
          if [ $(mount | grep -c "priv") != 1 ]
            then
               truecrypt -t -k "" -p $PW --protect-hidden=no --mount /media/wimac-drive02/data.p /home/$USER/priv/ &
        
               echo -e "--[ \e[1;32m unlocked removable \e[0m ]--"
               echo ""
        fi
    fi
     if [ -f ~/Dropbox/dat.enc ]; then
        echo $PW > /tmp/pwf
        #gpg -d --passphrase-file /tmp/pwf ~/Dropbox/dat.enc -o - > ~/Dropbox/dat.tgz
        openssl enc -d -aes-256-cbc -salt -in ~/Dropbox/dat.enc -out /tmp/dat.tgz -pass file:/tmp/pwf 
        tar xzf /tmp/dat.tgz
        srm ~/Dropbox/dat.enc /tmp/dat.tgz /tmp/pwf
        ln -s ~/.p ~/lpriv
    fi
        echo -e "--[ \e[1;32m unlocked local \e[0m ]--"
        echo ""
    
    }

umount()
{
    if [ -f /media/wimac-drive02/data.p ]; then
    while true; do
    read -p "Unmount Thumdrive? " yn
    case $yn in
        [Yy]* ) tdrive pumount; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
fi
}

while [ $# -gt 0 ]
do
   case "$1" in
       u|-u|--unlock)  ulock; exit 0; ;;
      -h|--help)       usage; exit 0; ;;
      -V|--version)    echo -n "$PROG version $VERSION "
                       echo 'Written by William J. MacLeod <wimac1@gmail.com>'
		               exit 0; ;;
        *)             usage; exit 1; ;;
   esac
   shift
done
plock
exit 0
