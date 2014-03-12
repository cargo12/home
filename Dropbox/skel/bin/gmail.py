#!/usr/bin/env python
import os
import string

#Enter your username and password below within double quotes
# eg. username="username" and password="password"
username="wimac1"
password="40ldfa5Tgole"

com="wget -O - https://%s:%s@mail.google.com/mail/feed/atom --no-check-certificate" % (username,password)

temp=os.popen(com)
msg=temp.read()
index=string.find(msg,"<fullcount>")
index2=string.find(msg,"</fullcount>")
fc=int(msg[index+11:index2])

if fc==0:
   print "0 new"
else:
   print str(fc)+" new"
