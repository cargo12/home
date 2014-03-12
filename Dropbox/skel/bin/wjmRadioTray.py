#!/usr/bin/python
#$Id: inetTrayRadio  06-16-2011 03:38PM William MacLeod (wimac1@gmail.com) ver: 12.206.1520
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

__author__= "William J. MacLeod"
__email__="wimac1@gmail.com"
__license__="GPL"

__version__="1.1.0"

debug = 0

import os,pynotify,gtk,feedparser

icons = os.path.expanduser('~/.icons/')

class SystrayIconApp:

    trayicon = os.path.expanduser('~/.icons/linux5.ico')

    def notifier(self,title,content,icon):
        n = pynotify.Notification(title,content,icon)
        n.show()

    # Update tray tool tip and icon
    def update(self,channel,chicon):
        self.tray.set_from_file(chicon)
        self.tray.set_tooltip(channel)

    def killshit(self):
        if self.toggle == 1:
            self.toggle = 0
            if debug == 1:
                print 'killing shit'
            os.system('killall mplayer')
            os.system('killall -9 vlc')
        else:
            self.toggle = 1
            os.system('killall mplayer')
            os.system('killall -9 vlc')

    def player(self,net,channel):
        self.killshit()
        if net == 'twit':
            self.icon = icons + 'twit.png'
            if debug == 1:
                print 'playing twit'
            os.system("mplayer -really-quiet -cache 8912 -cache-min 4 -aspect 16:9 %s >/dev/null &"% channel)
            #os.system("cvlc --aspect-ratio 16:9 %s >/dev/null&"% channel)
        if net == 'sirius':
            self.icon = icons + 'sirius.png'
            if debug == 1:
                print 'playing sirius'
            os.system("pyxis %s &"% channel)
        if net == 'rev3':
            self.icon = icons + 'rev3.png'
            if debug ==1:
                print 'playing rev3'
            os.system("mplayer -really-quiet -cache 1024 -cache-min 20 -aspect 16:9 %s >/dev/null &"% channel)
            #os.system("cvlc --aspect-ratio 16:9 -v 0 %s >/dev/null&"% channel)

    def feeder(self,av,feed):
        f=feedparser.parse(feed)
        #os.system('wget '+ f.feed.image['href'])
        self.title = f.feed.title
        self.desc = f.feed.description
        self.tray.set_tooltip((self.title))
        if av == 'v':
            ev=f.entries[0].enclosures[0]
            self.stream= ev.href
            #self.notifier(f.feed.title, f.entries[0].title, self.ficon)
        if av == 'a':
            e=f.entries[0]
            self.stream = e.link
            #self.notifier(f.feed.title, f.entries[0].title, self.ficon)

    # Shutdown
    def inetOff(self, widget):
        self.toggle = 1
        self.killshit()
        self.update('iNetRadio',self.trayicon)

    # Cancel/exit
    def delete_event(self, widget, event, data=None):
        self.killshit()
        gtk.main_quit()
        return False

   # Now Playing
    def nowplaying(self,widget):
        print self.title
        print self.desc
        #self.notifier(self.title,self.desc,self.ficon)

    # TWiT Live
    def twitlivev(self, widget):
        net='twit'
        self.ficon = icons + 'twitlive.gif'
        #self.stream = 'http://iphone-streaming.ustream.tv/ustreamVideo/1524/streams/live/playlist.m3u8'
        #self.stream = 'http://usher.justin.tv/stream/multi_playlist/twit.m3u'
        #self.stream ='http://www.ustream.tv/leolaporte'
        #self.stream ='http://bglive-a.bitgravity.com/twit/live/low'
        #self.stream ='http://bgmp-w.bitgravity.com/cdn-live-s1/_definst_/twit/live/low/playlist.m3u8'
        self.stream = 'http://twit.live-s.cdn.bitgravity.com/cdn-live-s1/_definst_/twit/live/high/playlist.m3u8'
        self.title = 'TWiT Live'
        self.player(net,self.stream)
        #self.notifier("TWiT","Live Video",self.ficon)
        self.update(self.title,self.icon)

    def twitlivea(self, widget):
        net='twit'
        stream='http://twit.am/listen'
        self.player(net,stream)
        #self.notifier("TWiT","Live Audio", self.icon)
        self.update('TWiT Video',self.icon)

    # TWiT
    def twitv(self, widget):
        net='twit'
        self.ficon = icons + 'twit-150x150.png'
        self.feeder('v','http://feeds.twit.tv/twit_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    def twita(self, widget):
        net='twit'
        self.ficon = icons + 'twit600audio.jpg'
        self.feeder('a','http://leoville.tv/podcasts/twit.xml')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # TNT
    def tntv(self, widget):
        net='twit'
        self.ficon = icons + 'tnt.jpg'
        self.feeder('v','http://feeds.twit.tv/tnt_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    def tnta(self, widget):
        net='twit'
        self.ficon = icons + 'tnt.jpg'
        icon = icons + 'twit.png'
        self.feeder('a','http://leoville.tv/podcasts/tnt.xml')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # The Tech Guy
    def ttgv(self, widget):
        net='twit'
        self.ficon = icons + 'ttg.jpg'
        self.feeder('v','http://feeds.twit.tv/ttg_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    def ttga(self, widget):
        net='twit'
        self.ficon = icons + 'ttg.jpg'
        self.feeder('a','http://leoville.tv/podcasts/ttg.xml')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # Security Now
    def snv(self, widget):
        net='twit'
        self.ficon = icons + 'sn600audio.jpg'
        self.feeder('v','http://feeds.twit.tv/sn_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    def sna(self, widget):
        net='twit'
        self.ficon = icons + 'sn600audio.jpg'
        self.feeder('a','http://leoville.tv/podcasts/sn.xml')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # TWiG
    def twigv(self, widget):
        net='twit'
        self.ficon = icons + 'twig200.jpg'
        self.feeder('v','http://feeds.twit.tv/twig_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    def twiga(self, widget):
        net='twit'
        self.ficon = icons + 'twig200.jpg'
        self.feeder('a','http://leoville.tv/podcasts/twig.xml')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

   # All About Android
    def aaav(self, widget):
        net='twit'
        self.ficon = icons + 'aaa.jpg'
        self.feeder('v','http://feeds.twit.tv/aaa_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    def aaaa(self, widget):
        net='twit'
        self.ficon = icons + 'aaa.jpg'
        self.feeder('a','http://leoville.tv/podcasts/aaa.xml')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # FLOSS Weekly
    def flossv(self, widget):
        net='twit'
        self.ficon = icons + 'aaa.jpg'
        self.feeder('v','http://feeds.twit.tv/floss_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # TWiET
    def twiet(self, widget):
        net='twit'
        self.ficon = icons + 'twiet.jpg'
        self.feeder('v','http://feeds.twit.tv/twiet_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # Giz Wiz
    def dgwv(self, widget):
        net='twit'
        self.ficon = icons + 'dgw.jpg'
        self.feeder('v','http://feeds.twit.tv/dgw_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    #Before you buy!
    def byb(self, widget):
        net='twit'
        self.ficon = icons + 'byb.jpg'
        self.feeder('v','http://feeds.twit.tv/byb_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    #Know How
    def kh(self, widget):
        net='twit'
        self.ficon = icons + 'kh.jpg'
        self.feeder('v','http://feeds.twit.tv/kh_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    #Frame Rate
    def fr(self, widget):
        net='twit'
        self.ficon = icons + 'fr.jpg'
        self.feeder('v','http://feeds.twit.tv/fr_video_small')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # Revision3 podcasts
    # Tekzilla
    def tekzilla(self, widget):
        net='rev3'
        self.ficon = icons + 'tekzilla.jpg'
        self.feeder('v','http://revision3.com/tekzilla/feed/MP4-Large?subshow=false')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # Hak5
    def hak5(self, widget):
        net='rev3'
        self.ficon = icons + 'hak5.jpg'
        self.feeder('v','http://revision3.com/hak5/feed/MP4-Large?subshow=false')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)

    # The Ben Heck Show
    def tbhs(self, widget):
        net='rev3'
        self.ficon = icons + 'tbhs.jpg'
        self.feeder('v','http://revision3.com/tbhs/feed/MP4-Large?subshow=false')
        self.player(net,self.stream)
        self.update(self.title ,self.icon)


    # Sirius channels (pryxis and sirius accout required)
    # Howard
    def howard(self, widget):
        net='sirius'
        channel = 'Howard 100'
        self.player(net,channel)
        self.update(channel,self.icon)

    # Howard 101
    def howard101(self, widget):
        net='sirius'
        channel = 'Howard 101'
        self.player(net,channel)
        self.update(channel,self.icon)

    # Faction
    def faction(self, widget):
        net='sirius'
        channel = 'Faction'
        self.player(net,channel)
        self.update(channel,self.icon)

    # Playboy
    def playboy(self, widget):
        net='sirius'
        channel = 'Playboy Radio'
        self.player(net,channel)
        self.update(channel,self.icon)

    def __init__(self):
        self.toggle = 0
        self.title=''
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file(self.trayicon)
        self.tray.connect('popup-menu',self.on_right_click)
        self.tray.connect('activate',self.on_left_click)
        self.tray.connect('scroll-event', self.scrollEvent)
        self.tray.set_tooltip(('wjmRadioTray'))

    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)

    def on_left_click(self,widget):
        os.system('sudo xfce4-mixer')

    def scrollEvent(self, widget, event):
        mixer = 'amixer -q -v 0'
        if event.direction == gtk.gdk.SCROLL_UP:
            os.system('amixer -q set Master 5dB+')
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            os.system('amixer -q set Master 5dB-')

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

        self.item6 = gtk.MenuItem("TWiT Live (video)")
        self.item6.connect('activate', self.twitlivev)
        self.item6.show()
        menu.append(self.item6)

        self.item11 = gtk.MenuItem("TWiT Live (audio)")
        self.item11.connect('activate', self.twitlivea)
        self.item11.show()
        menu.append(self.item11)

        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        #self.item9 = gtk.MenuItem('Howard 100')
        #self.item9.connect('activate', self.howard)
        #self.item9.show()
        #menu.append(self.item9)

        self.item1 = gtk.MenuItem('TNT (video)')
        self.item1.connect('activate', self.tntv)
        self.item1.show()
        menu.append(self.item1)

        self.item9 = gtk.MenuItem('TNT (audio)')
        self.item9.connect('activate', self.tnta)
        self.item9.show()
        menu.append(self.item9)

        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        self.item2 = gtk.MenuItem("TWiT (video)")
        self.item2.connect('activate', self.twitv)
        self.item2.show()
        menu.append(self.item2)

        self.item5 = gtk.MenuItem("TWiT (audio)")
        self.item5.connect('activate', self.twita)
        self.item5.show()
        menu.append(self.item5)

        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        self.item13 = gtk.MenuItem("Tech Guy (video)")
        self.item13.connect('activate', self.ttgv)
        self.item13.show()
        menu.append(self.item13)

        self.item14 = gtk.MenuItem("Tech Guy (audio)")
        self.item14.connect('activate', self.ttga)
        self.item14.show()
        menu.append(self.item14)

        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        self.item10 = gtk.MenuItem('All About Android (video)')
        self.item10.connect('activate', self.aaav)
        self.item10.show()
        menu.append(self.item10)

        self.item18 = gtk.MenuItem("Before you buy! (video)")
        self.item18.connect('activate', self.byb)
        self.item18.show()
        menu.append(self.item18)

        self.item19 = gtk.MenuItem("Daily Giz Wiz (video)")
        self.item19.connect('activate', self.dgwv)
        self.item19.show()
        menu.append(self.item19)

        self.item3 = gtk.MenuItem("Security Now (audio)")
        self.item3.connect('activate', self.sna)
        self.item3.show()
        menu.append(self.item3)

        self.item8 = gtk.MenuItem("TWiG (video)")
        self.item8.connect('activate', self.twigv)
        self.item8.show()
        menu.append(self.item8)
        
        self.item23 = gtk.MenuItem("TWiET (video)")
        self.item23.connect('activate', self.twiet)
        self.item23.show()
        menu.append(self.item23)

        self.item10 = gtk.MenuItem('FLOSS Weekly (video)')
        self.item10.connect('activate', self.flossv)
        self.item10.show()
        menu.append(self.item10)

        self.item21 = gtk.MenuItem('Frame Rate (video)')
        self.item21.connect('activate', self.fr)
        self.item21.show()
        menu.append(self.item21)

        self.item27 = gtk.MenuItem('Know How (video)')
        self.item27.connect('activate', self.kh)
        self.item27.show()
        menu.append(self.item27)

        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        self.item12 = gtk.MenuItem("Tekzilla")
        self.item12.connect('activate', self.tekzilla)
        self.item12.show()
        menu.append(self.item12)

        self.item13 = gtk.MenuItem("Hak5")
        self.item13.connect('activate', self.hak5)
        self.item13.show()
        menu.append(self.item13)

        self.item16 = gtk.MenuItem("Ben Heck Show")
        self.item16.connect('activate', self.tbhs)
        self.item16.show()
        menu.append(self.item16)


        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        self.item15 = gtk.MenuItem("Now Playing")
        self.item15.connect('activate', self.nowplaying)
        self.item15.show()
        menu.append(self.item15)

        #kills everything need to make a check to see if running before activation new channel
        self.item7 = gtk.MenuItem("Shutdown")
        self.item7.connect('activate', self.inetOff)
        self.item7.show()
        menu.append(self.item7)

        self.seperator1 = gtk.MenuItem()
        self.seperator1.show()
        menu.append(self.seperator1)

        #self.quit = gtk.MenuItem("Quit")
        self.quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.quit.connect('activate', self.delete_event, "Get me out of here")
        self.quit.show()
        menu.append(self.quit)

        menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.tray)

if __name__=="__main__":
    SystrayIconApp()
    gtk.main()
