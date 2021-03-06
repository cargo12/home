#!/usr/bin/python
# -*- coding: utf-8 -*-
# Eli Criffield < pyeli AT zendo DOT net >
# Licensed under GPLv2 See: http://www.gnu.org/licenses/gpl.txt

import Sipie
import os
import time
import sys

def playlistLog(logme):
    date = time.strftime('%Y%m%d%H')
    file = '%s/%s-%s.playlist'%(outputdir,stream,date)
    fd = open(file,'a')
    fd.write('%s\n'%logme)
    fd.close()


stream = sys.argv[1]
hoursToRecord = int(sys.argv[2])
if len(sys.argv) > 3:
    skip = int(sys.argv[3]) # mins to skip at start
else:
    skip = 0

#This is the directory the config files will be
config = Sipie.Config(os.path.expanduser('~/.sipie/'))

# There's a class for mplayer xine and windows media player
# Also gstream in gnome, but haven't tested it
streamHandler = Sipie.mplayerHandler('/usr/bin/mplayer')

day = time.strftime('%Y%m%d')
outputdir = os.path.expanduser('/space/media/sirius/%s/'%day)

if not os.path.isdir(outputdir):
    os.mkdir(outputdir)

gencmd = lambda hour: '/usr/bin/mplayer -slave -really-quiet -nojoystick -nolirc -user-agent NSPlayer -nomouseinput -prefer-ipv4 -cache 32 -dumpstream -dumpfile %s/%s-%s%s.wmv -playlist '%(outputdir,stream,day,hour) 

sipie = Sipie.Player(config.items())
sipie.setPlayer(streamHandler)

time.sleep(skip * 60)

for cnt in xrange(hoursToRecord): 
    # pick a stream, you can see all avalibe with sipie.getStreams()
    hour = time.strftime('%H')
    sipie.setStream(stream)
    streamHandler.command = gencmd(hour)
    #Play it
    sipie.play()
    minsToSleep = 60

    if cnt == 0:
        minsToSleep = minsToSleep - skip

    for x in xrange(minsToSleep):
        # Hey whats playing on the stream i selected?
        for y in xrange(2):
            playing = sipie.nowPlaying()
            if playing['new']:
                playlistLog(playing['logfmt'])
            time.sleep(30)
            
    sipie.close()
