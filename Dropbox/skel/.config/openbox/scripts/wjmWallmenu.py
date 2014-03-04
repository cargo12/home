#!/usr/bin/env python

import os
import re
import string
import sys
from os.path import isdir

# types of files accepted (list, seperated by a |)
filetypes = "jpg|png|gif"
# directory where wallpapers are stored (must be long: no ~ symbol allowed)
directory = "/home/wimac/images/backgrounds/"
# program to set wallpaper
program = "wjmWallpaper.py"

def genmenu(start, directory):
	# get a directory list
	dirlist = os.listdir(directory)
	dirlist.sort()
	for d in dirlist:
		# set di to overall directory
		di = directory + "/" + d
		# if we get a dir, generate a menu
		if isdir(di):
			print ""
			print "  <menu id=\"" + di + "\" label=\"" + d + "\" >"
			genmenu(start, di)
			print "  </menu>"
		# if we get a file, check if it is a valid type
		else:
			if re.search(filetypes, string.lower(di)) > 0:
				# make fi variable just filename, without extension
				fi = string.replace(string.replace(di, directory, ""), "/", "")
				fi = fi[:string.rfind(fi, ".")]
				# if so, add it to the pipe menu
				print "  <item label=\"" + fi + "\">"
				# execute line to set wallpaper
				print "    <action name=\"Execute\"><execute>" + program + " \"" + di + "\"</execute></action>"
				# if we want to update config file, do so
				print "  </item>"

def main(argv):
    print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    print "<openbox_pipe_menu>"
    # set the original start directory
    start = directory
    # generate menu
    genmenu(start, directory)
    # end menu
    print "</openbox_pipe_menu>"

# run the main() function		
if __name__ == "__main__":
	main(sys.argv[1:])
