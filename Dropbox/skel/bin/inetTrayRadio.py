#!/usr/bin/python
#$Id: inetTrayRadio  06-16-2011 03:38PM William MacLeod (wimac1@gmail.com) ver: 12.018.1709
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


import os,pynotify,gtk,feedparser

class SystrayIconApp:

    trayicon = '/home/wimac/Dropbox/gfx/icons/linux5.ico'

    # Update tray tool tip and icon
    def update(self,channel,chicon):
        #self.tray=gtk.StatusIcon()
        self.tray.set_from_file(chicon)
        self.tray.set_tooltip(channel)

    def killshit(self):
        os.system('killall mplayer')

    # Shutdown
    def inetOff(self, widget):
        self.killshit()
        self.update('iNetRadio',self.trayicon)

    # Cancel/exit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        os.system("killall mplayer && killall pyxis")
        return False

    # generic video from TWiT network arg is feed
    def twitnet(self, widget, feed):
        f=feedparser.parse(feed)
        ficon = '/home/wimac/bin/twit-150x150.png'
        #os.system('wget '+ f.feed.image['href'])
        icon = '/home/wimac/bin/twit.png'
        ev=f.entries[0].enclosures[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer -really-quiet ' + ev.href + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # TWiT Video
    def twitvideo(self, widget):
        f=feedparser.parse('http://feeds.twit.tv/twit_video_small')
        ficon = '/home/wimac/bin/twit-150x150.png'
        #os.system('wget '+ f.feed.image['href'])
        icon = '/home/wimac/bin/twit.png'
        ev=f.entries[0].enclosures[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer -really-quiet ' + ev.href + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # TNT Video
    def tntvideo(self, widget):
        f=feedparser.parse('http://feeds.twit.tv/tnt_video_small')
        ficon = '/home/wimac/bin/tnt-150x150.png'
        icon = '/home/wimac/bin/twit.png'
        ev=f.entries[0].enclosures[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer -really-quiet ' + ev.href + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # TNT
    def tnt(self, widget):
        f=feedparser.parse('http://leoville.tv/podcasts/tnt.xml')
        ficon = '/home/wimac/bin/tnt600audio.jpg'
        #os.system('wget '+ f.feed.image['href'])
        icon = '/home/wimac/bin/twit.png'
        e=f.entries[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer -really-quiet ' + e.link + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # Security Now
    def sn(self, widget):
        f=feedparser.parse('http://leoville.tv/podcasts/sn.xml')
        ficon = '/home/wimac/bin/sn600audio.jpg'
        icon = '/home/wimac/bin/twit.png'
        e=f.entries[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer -really-quiet ' + e.link + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # TWiG
    def twig(self, widget):
        f=feedparser.parse('http://leoville.tv/podcasts/twig.xml')
        ficon = '/home/wimac/bin/twig200.jpg'
        icon = '/home/wimac/bin/twit.png'
        e=f.entries[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer ' + e.link + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # TWiT
    def twit(self, widget):
        f=feedparser.parse('http://leoville.tv/podcasts/twit.xml')
        ficon = '/home/wimac/bin/twit600audio.jpg'
        icon = '/home/wimac/bin/twit.png'
        e=f.entries[0]
        n = pynotify.Notification(f.feed.title, f.entries[0].title, ficon)
        n.show()
        os.system('mplayer -really-quiet ' + e.link + ' >/dev/null &')
        self.update(f.feed.title ,icon)

    # Howard
    def howard(self, widget):
        title = 'Howard 100'
        icon = '/home/wimac/bin/sirius.png'
        os.system("pyxis 'howard 100'&")
        self.update(title,icon)

    # Howard 101
    def howard101(self, widget):
        os.system("pyxis 'howard 101'&")

    # Faction
    def faction(self, widget):
        os.system("pyxis 'faction'&")

    # Playboy
    def playboy(self, widget):
        os.system("pyxis 'playboy radio'&")

    # TWiT Live
    def twitlive(self, widget):
        icon = '/home/wimac/bin/twit.png'
        n = pynotify.Notification("TWiT","Live Video", icon)
        n.show()
        self.update('TWiT Video',icon)
        os.system("mplayer -really-quiet -cache 32 -cache-min 4 -aspect 16:9 http://bglive-a.bitgravity.com/twit/live/low >/dev/null &")

    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file(self.trayicon)
        self.tray.connect('popup-menu',self.on_right_click)
        self.tray.connect('scroll-event', self.scrollEvent)
        self.tray.set_tooltip(('inetRadio'))

    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)

    def scrollEvent(self, widget, event):
        mixer = 'amixer -q -v 0'
        if event.direction == gtk.gdk.SCROLL_UP:
            os.system('amixer -q set Master 5dB+')
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            os.system('amixer -q set Master 5dB-')

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

        self.item6 = gtk.MenuItem("TWiT Live")
        self.item6.connect('activate', self.twitlive)
        self.item6.show()
        menu.append(self.item6)

        self.seperator = gtk.MenuItem()
        self.seperator.show()
        menu.append(self.seperator)

        self.item9 = gtk.MenuItem('Howard 100')
        self.item9.connect('activate', self.howard)
        self.item9.show()
        menu.append(self.item9)

        self.item1 = gtk.MenuItem('TNT Video')
        self.item1.connect('activate', self.tntvideo)
        self.item1.show()
        menu.append(self.item1)

        self.item2 = gtk.MenuItem("TWiT Video")
        self.item2.connect('activate', self.twitvideo)
        self.item2.show()
        menu.append(self.item2)

        self.item3 = gtk.MenuItem("Security Now")
        self.item3.connect('activate', self.sn)
        self.item3.show()
        menu.append(self.item3)

        self.item4 = gtk.MenuItem("TNT")
        self.item4.connect('activate', self.tnt)
        self.item4.show()
        menu.append(self.item4)

        self.item5 = gtk.MenuItem("TWiT")
        self.item5.connect('activate', self.twit)
        self.item5.show()
        menu.append(self.item5)

        self.item8 = gtk.MenuItem("TWiG")
        self.item8.connect('activate', self.twig)
        self.item8.show()
        menu.append(self.item8)

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
