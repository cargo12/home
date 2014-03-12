#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os

class inetRadio:

    # Cancel/exit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    # Howard 
    def howard(self, widget):
        os.system("pyxis 'howard 100'&")

    # Howard 101
    def howard101(self, widget):
        os.system("pyxis 'howard 101'&")
    
    # Faction
    def faction(self, widget):
        os.system("pyxis 'faction'&")
    
    # Playboy
    def playboy(self, widget):
        os.system("pyxis 'playboy radio'&")

    # TWiT
    def twit(self, widget):
        os.system("mplayer http://twit.am:80/listen &")
   
    # TWiT Video
    def twitlive(self, widget):
        os.system("mplayer -aspect 16:9 http://bglive-a.bitgravity.com/twit/live/low &")


    # Shutdown
    def inetOff(self, widget):
        os.system("killall mplayer && killall pyxis")

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Will is a stinky poo poo butt")
        self.window.set_resizable(False)
        self.window.set_position(1)
        self.window.connect("delete_event", self.delete_event)
        #self.window.set_border_width(20)

        # Create a box to pack widgets into
        self.box1 = gtk.HBox(False, 0)
        self.window.add(self.box1)

        # Create cancel button
        self.button1 = gtk.Button("X")
        self.button1.set_border_width(15)
        self.button1.connect("clicked", self.delete_event, "Changed me mind :)")
        self.box1.pack_start(self.button1, True, True, 0)
        self.button1.show()

        # Create howard button
        self.button2 = gtk.Button("_Howard")
        self.button2.set_border_width(5)
        self.button2.connect("clicked", self.howard)
        self.box1.pack_start(self.button2, True, True, 0)
        self.button2.show()

        # Create howard 101 button
        self.button3 = gtk.Button("Howard _101")
        self.button3.set_border_width(5)
        self.button3.connect("clicked", self.howard101)
        self.box1.pack_start(self.button3, True, True, 0)
        self.button3.show()

        # Create faction button
        self.button4 = gtk.Button("_Faction")
        self.button4.set_border_width(5)
        self.button4.connect("clicked", self.faction)
        self.box1.pack_start(self.button4, True, True, 0)
        self.button4.show()

         # Create playboy button
        self.button5 = gtk.Button("_Playboy")
        self.button5.set_border_width(5)
        self.button5.connect("clicked", self.playboy)
        self.box1.pack_start(self.button5, True, True, 0)
        self.button5.show()

         # Create TWiT button
        self.button6 = gtk.Button("_TWiT")
        self.button6.set_border_width(5)
        self.button6.connect("clicked", self.twit)
        self.box1.pack_start(self.button6, True, True, 0)
        self.button6.show()

        # Create TWiT button
        self.button7 = gtk.Button("_TWiT Live")
        self.button7.set_border_width(5)
        self.button7.connect("clicked", self.twitlive)
        self.box1.pack_start(self.button7, True, True, 0)
        self.button7.show()
 
        # Create shutdown button
        self.button8 = gtk.Button("_SatOff")
        self.button8.set_border_width(5)
        self.button8.connect("clicked", self.inetOff)
        self.box1.pack_start(self.button8, True, True, 0)
        self.button8.show()

        self.box1.show()
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    gogogo = inetRadio()
    main()
