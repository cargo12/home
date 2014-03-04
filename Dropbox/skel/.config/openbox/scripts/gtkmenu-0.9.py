#!/usr/bin/env python

import os
import string
import sys
from os.path import isdir

# ---------------------------------- About ------------------------------------ #
# This file inserts a GTK theme pipe menu into Openbox.				#
#										#
# Author: Pwnz3r - http://pstudios.ath.cx					#
#										#
#										#
# ------------------------------ Setting it up -------------------------------- #
# Put this script in ~/.config/openbox/scripts.					#
#										#
# ------------------------------ Configuration -------------------------------- #
# Here is the chance for some more configuration.				#
font = "Verdana 9" # Change this to the font of your choice.			#
#										#
# ----------------------------------------------------------------------------- #

def buildMenu(directory, menuName):
	dirlist = os.listdir(directory)

	# Fork the Menu
	print "<menu id=\"g" + menuName + "\" label=\"" + menuName + "\">"
	for t in dirlist:
		# The overall directory
		tpath = directory + "/" + t

		# Check if it is a directory
		if isdir(tpath):
			listing = os.listdir(tpath)
			if "gtk-2.0" in listing:
				print "  <item label=\"" + t + "\">"
				if menuName == "User Themes":
					print "    <action name=\"Execute\"><execute>~/.config/openbox/scripts/gtkmenu.py -s \"~/.themes/" + t + "/gtk-2.0/gtkrc\"</execute></action>"
				if menuName == "System Themes":
					print "    <action name=\"Execute\"><execute>~/.config/openbox/scripts/gtkmenu.py -s \"/usr/share/themes/" + t + "/gtk-2.0/gtkrc\"</execute></action>"
				print "  </item>"
	print "</menu>"

def setTheme():
		gtkrc = file(os.getenv('HOME') + "/.gtkrc-2.0","w")
		gtkrc.write("# -- Theme updated by gtkmenu.py\n")
		gtkrc.write("include \"" + sys.argv[2] + "\"\n\n")
		gtkrc.write("style \"user-font\" {\n")
		gtkrc.write("	font_name = \"" + font + "\" } \n")
		gtkrc.write("}\n\n")
		gtkrc.write("widget_class \"*\" style \"user-font\" \n\n")
		gtkrc.write("gtk-font-name=\"" + font + "\" \n\n")
		gtkrc.write(os.getenv('HOME') + "/.gtkrc.mine\" \n")
		gtkrc.close()

def main():
	if sys.argv[1] == "-s":
		setTheme()
	elif sys.argv[1] == "-m":
		# Begin the menu
		print "<openbox_pipe_menu>"

		# User themes
		buildMenu(os.getenv('HOME') + "/.themes", "User Themes")

		# System themes
		buildMenu("/usr/share/themes", "System Themes")

		# End the menu
		print "</openbox_pipe_menu>"

# Get it all into motion
if __name__ == "__main__":
	main()
