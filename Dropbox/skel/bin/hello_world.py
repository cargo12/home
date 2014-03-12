#!/usr/bin/env python

# Load in pygtk and gtk

import pygtk
pygtk.require('2.0')
import gtk

# Define the main window

class Whc:
    def __init__(self):
# Window and framework
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)

# Box for multiple widgits
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)

# Three buttons
        self.button = gtk.Button("First Button")
        self.button.connect("clicked", self.hello, "Piano")
        self.box1.pack_start(self.button, True, True, 0)
        self.button.show()

        self.nextbutton = gtk.Button("Second Button")
        self.nextbutton.connect("clicked", self.hello, "Pineapple")
        self.box1.pack_start(self.nextbutton, True, True, 0)
        self.nextbutton.show()

        self.lastbutton = gtk.Button("Quit")
        self.lastbutton.connect("clicked", self.destroy)
        self.box1.pack_start(self.lastbutton, True, True, 0)
        self.lastbutton.show()

# Show the box
        self.box1.show()

# Show the window
        self.window.show()

# Callback function for use when the button is pressed

    def hello(self, widget, info):
        print "Button %s was pressed" % info
        print "Hello World"

# Destroy method causes appliaction to exit
# when main window closed

    def destroy(self, widget, data=None):
        gtk.main_quit()

# All PyGTK applications need a main method - event loop

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Whc()
    base.main()
