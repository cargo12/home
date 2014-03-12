#!/bin/bash
#$Id: status  08-09-2008 10:30AM v.08.222.1030 wimac Exp $
#Last modified: 08-09-2008  10:30AM wimac
while true;
do
date=`date +"%Y.%m.%d %l:%M" | sed 's/  / /g'`


### CPU
CPUSTAT="$HOME/.cpustat"
old_cpu_vals=(`head -1 "$CPUSTAT"`)
cpu_old_user=${old_cpu_vals[0]}
cpu_old_nice=${old_cpu_vals[1]}
cpu_old_system=${old_cpu_vals[2]}
cpu_old_idle=${old_cpu_vals[3]}
cpu_old_total=`echo "$cpu_old_user + $cpu_old_nice + $cpu_old_system + $cpu_old_idle" | bc`

cpu_vals_text=`cat /proc/stat  | head -1 | sed -e 's/^cpu[^0-9]*//g' -e 's/\([^ ]\+ [^ ]\+ [^ ]\+ [^ ]\+\).*/\1/g'`
cpu_vals=($cpu_vals_text)
cpu_user=${cpu_vals[0]}
cpu_nice=${cpu_vals[1]}
cpu_system=${cpu_vals[2]}
cpu_idle=${cpu_vals[3]}
cpu_total=`echo "$cpu_user + $cpu_nice + $cpu_system + $cpu_idle" | bc`
pcpu=`echo "(100 * ($cpu_system - $cpu_old_system + $cpu_user - $cpu_old_user)) / ($cpu_total - $cpu_old_total)" | bc`
echo $cpu_vals_text > "$CPUSTAT"


### MEMORY
mem_vals=`free -m | grep '^Mem:' | sed 's/Mem://g'`
mtot=`echo $mem_vals | sed 's/ .*//g'`
muse=`echo $(echo $mem_vals | cut -f2,5,6 -d" " | sed 's/ / - /g') | bc`
pmem=`echo "100 * $muse / $mtot" | bc`


### MPD
mpc_lines=`mpc | wc -l`
vol=`mpc | grep 'volume:' | sed -e 's/volume: //' -e 's/ .*//g'`
mpc_text="stopped @ $vol"
if [[ $mpc_lines -gt 1 ]]; then
    song=`mpc | head -1`
    status=`mpc | grep '^\[' | sed -e 's/ .*//' -e 's/[^a-zA-Z]//g'`
    mpc_text="$song @ $vol"
fi


### MAIL
if [ -f "$MAIL" ]; then
    mail_tot=`cat "$MAIL" | grep -c '^From '`
    mail_old=`cat "$MAIL" | grep '^Status: ' | grep -c 'O'`
    mail_new=`echo "$mail_tot-$mail_old" | bc`
    if [[ $mail_new -eq 0 ]]; then
        mail_new="-"
    fi
    if [[ $mail_tot -eq 0 ]]; then
        mail_tot="-"
    fi
    mail_text="$mail_new/$mail_tot"
else
    mail_text="-/-"
fi


### UPTIME
uptime=`uptime | sed 's/.* \([0-9]\+ days\).*/\1/' | tr -d '[ a-zA-z]'`


### SWAP
swap_vals=`free | grep 'Swap: ' | sed 's/.*: *\([0-9]\+\) \+\([0-9]*\).*/\1 \2/'`
swap_tot=`echo $swap_vals | cut -f1 -d" "`
swap_use=`echo $swap_vals | cut -f2 -d" "`
pswap=`echo "100*$swap_use / $swap_tot" | bc`

echo 0 widget_tell tb_mpc "$mpc_text" | awesome-client
echo 0 widget_tell g_cpu "$pcpu" | awesome-client
echo 0 widget_tell tb_mem "$pmem%" | awesome-client
echo 0 widget_tell pb_mem "$pmem" | awesome-client
echo 0 widget_tell tb_date "$date" | awesome-client

sleep 3
done


