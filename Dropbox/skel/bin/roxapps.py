#!/usr/bin/python

import sys
import os.path

print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
print "<openbox_pipe_menu>"

def scan( menu_path ):

        mylist = os.listdir( menu_path )
        mylist.sort()

        filelist = []
        appdirlist = []
        dirlist = []
        for name in mylist:
                fullname = os.path.join( menu_path, name )
                fullappdir = os.path.join( fullname,"AppRun" )
                if os.path.isfile( fullname ):
                        if name <> ".DirIcon":
                                filelist.append( "<item label=\"" + name + "\"><action name=\"Execute\"><execute>rox \"" \
                                + fullname + "\"</execute></action></item>" )
                elif os.path.isdir( fullname ):
                        if os.path.exists( fullappdir ):
                                appdirlist.append( "<item label=\"" + name + "\"><action name=\"Execute\"><execute>" \
                                + fullappdir + "</execute></action></item>" )
                        else:
                                dirlist.append( name )

        for f in filelist:
                print f

        for a in appdirlist:
                print a

        for d in dirlist:
                fullname = os.path.join( menu_path, d )
                print "<menu id=\"" + d + "\" label=\"" + d + "\">"
                scan( fullname )
                print "</menu>"

scan ( sys.argv[1] )

print "</openbox_pipe_menu>"


