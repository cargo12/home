#!/bin/bash
# Script name:  obmpc.sh
# Requirement:  mpc
# Author:       straivir@ucsd.edu AKA grad_guy 
# License:      GPL 2.0

# INSTALLATION
# 1. Put this script in /usr/bin/ and chmod +x /usr/bin/obmpc.sh
# 2. Add <menu id="obmpc" label="OBMPC" execute="obmpc.sh" /> in menu.xml
# 3. Add <menu id="obmpc" /> inside your openbox root-menu

# NOTE
# Adjusting Volume needs repeating action, so IMHO it's not a good idea for pipe Menu.
# Anyhow, it's very easy to add Volume control.

# SETUP
tmp=/tmp/.obmpc
chop=20
# END SETUP

chopmore=$((chop + 1))
chopless=$((chop - 1))
mpc playlist > $tmp
count=`cat $tmp | wc -l`
nowwhat=`mpc | head -n 1 | sed -e 's/\&/&amp;/g'`
nowstatus=`mpc | grep '#' | cut -d '/' -f1`
whatnow=`mpc | tail -n 1`

submenu ()
{
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
echo "<openbox_pipe_menu>"
for ((a=$1; a <= $2 ; a++))
do
    name=`cat $tmp | grep "#$a)" | sed -e 's/(//g' | sed -e 's/)//g' | sed -e 's/\#//g' | sed -e 's/\&/&amp;/g'`
    echo "  <item label=\"$name\">"
    echo "    <action name=\"Execute\"><execute>mpc play $a</execute></action>"
    echo "  </item>"
done
echo "</openbox_pipe_menu>"
}

pack ()
{
echo "  <menu id=\"obmpc$2\" label=\"Track $1-$2\" execute=\"obmpc.sh $1 $2\" />"
}

controlmenu ()
{
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
echo "<openbox_pipe_menu>"
echo "  <item label=\"MPC Prev\">"
echo "    <action name=\"Execute\"><execute>mpc prev</execute></action>"
echo "  </item>"
echo "  <item label=\"MPC Play\">"
echo "    <action name=\"Execute\"><execute>mpc play</execute></action>"
echo "  </item>"
echo "  <item label=\"MPC Pause\">"
echo "    <action name=\"Execute\"><execute>mpc pause</execute></action>"
echo "  </item>"
echo "  <item label=\"MPC Stop\">"
echo "    <action name=\"Execute\"><execute>mpc stop</execute></action>"
echo "  </item>"
echo "  <item label=\"MPC Next\">"
echo "    <action name=\"Execute\"><execute>mpc next</execute></action>"
echo "  </item>"
echo "  <separator />"
echo "  <item label=\"Toggle Repeat\">"
echo "    <action name=\"Execute\"><execute>mpc repeat</execute></action>"
echo "  </item>"
echo "  <item label=\"Toggle Random\">"
echo "    <action name=\"Execute\"><execute>mpc random</execute></action>"
echo "  </item>"
echo "</openbox_pipe_menu>"
}

if [ -z "$1" ]
then
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    echo "<openbox_pipe_menu>"
    echo "  <item label=\"$nowstatus $nowwhat\">"
    echo "    <action name=\"Execute\"><execute>mpc toggle</execute></action>"
    echo "  </item>"
    echo "  <menu id=\"obmpc-control\" label=\"Control\" execute=\"obmpc.sh control\" />"
    echo "  <separator />"
    if [ "$count" -lt "$chopmore" ]
    then
        pack 1 $count
    else
        p=1
        q=$chop
        while [ "$q" -lt "$count" ]
        do
            pack $p $q
            p=$((p + chop))
            q=$((q + chop))
        done
        qq=$((q - chopless))
        pack $qq $count
    fi
    echo "  <separator />"
    echo "  <item label=\"$whatnow\">"
    echo "    <action name=\"Execute\"><execute>mpc toggle</execute></action>"
    echo "  </item>"
    echo "</openbox_pipe_menu>"
fi

if [ "$#" -eq 2 ]
then
    submenu $1 $2
fi

if [ "$1" = control ]
then
    controlmenu
fi
