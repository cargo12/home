#!/bin/sh
echo "<openbox_pipe_menu>"
echo "    <item label=\"new session\">"
echo "        <action name=\"execute\">"
echo "            <command>gdmflexiserver</command>"
echo "        </action>"
echo "    </item>"
echo "    <separator />"

who | awk '{
print "    <item label=\"" $1 " - " $2 "\">";
print "        <action name=\"Execute\">";
if ($2 ~ /tty[0-9]+/)
    print "            <command>sudo chvt " substr($2,4) "</command>";
if ($2 ~ /:[0-9]+/) {
    print "            <command>sudo chvt $(ps -C Xorg -o tty,cmd | \\";
    print "                     grep " $2 " | \\"
    print "                     sed \"s/^tty\\([0-9]\\+\\).*$/\\1/\")";
    print "            </command>";
}
print "        </action>";
print "    </item>";
}'

echo "</openbox_pipe_menu>"
