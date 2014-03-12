#! /bin/bash

export PATH=$PATH:/sbin:/usr/sbin:/bin:/usr/bin

base=`dirname "$0"`
inlog="$base/forticlientsslvpn.install.log"
usr=`id -u`
daemon="$base/fctsslvpndaemon"

if [ "$1" == "1" ]; then
	echo "run myself in xterm..." >> $inlog
	xterm -e "$0" 2
	st=$?
	exit $st
fi

if [ "$usr" != "0" ]; then
# we are running in xterm now.
	rm -rf "$base/.nolicense"
	sudo "$0" 3
	if [ -f "$base/.nolicense" ]; then
		exit 0
	fi
	if [ ! -u "$daemon" ]; then
		echo "sudo failed, use su instead..." >> $inlog
		echo "it seems that 'sudo' does not work here, try to use 'su'"
		su -c "\"$0\" 4"
	fi
	if [ ! -u "$daemon" ]; then
		echo "auth failed" >> $inlog
		exit -1
	fi
	exit 0
fi

echo "begin setup at $base..." >> $inlog
more "$base/License.txt"
echo -n "Do you agree with this license ?[Yes/No]"
read ans
yn=`echo $ans|sed '
s/y/Y/
s/e/E/
s/s/S/
'`
if [ "$yn" != "YES" -a "$yn" != "Y" ]; then
	touch "$base/.nolicense"
	chmod a+w "$base/.nolicense"
	echo "Do not agree with this license, aborting..."
	exit 0
fi

if [ ! -f /etc/ppp/options ]; then
	echo "Create /etc/ppp/options" >> $inlog
	touch /etc/ppp/options
fi

if [ ! -f "$daemon" ]; then
	echo "The installation package is broken, give up!"
	echo "The installation package is broken, give up!" >> $inlog
	exit -1
fi

echo -n "Checking if pppd is installed..." >> $inlog

if [ ! -x /usr/sbin/pppd ]; then
	echo "pppd is not installed" >> $inlog
	echo "Please install pppd, it is required by FortiClient SSL VPN!"
	exit -1
fi
echo "OK" >> $inlog

echo -n "Checking if iproute package is installed..." >> $inlog
if [ ! -x /sbin/ip -a ! -x /bin/ip -a ! -x /usr/bin/ip -a ! -x /usr/sbin/ip ]; then
	echo "iproutes utility is not installed" >> $inlog
	echo "Please install the iproutes utility, it is required by FortiClient SSL VPN"
	exit -1
fi
echo "OK" >> $inlog

echo "Setup $daemon" >> $inlog

chown root "$daemon"
chgrp root "$daemon"
chmod a-w "$daemon"
chmod u+s "$daemon"
chmod a+x "$daemon"

chmod a+x "$base/sysconfig.linux.sh" "$base/cleanup.linux.sh"

