#!/usr/bin/env python
#$Id: wjmWallpaper  07-16-2011 02:56PM wimac(wimac1@gmail.com) ver: 11.212.1624
#
#wallpaper changer
import sys, os, shutil

home = os.path.expanduser('~/')
wpaper = '.background'
cmd = 'feh --bg-fill '
wpaper = home + wpaper

def wpchange(nwpaper):
    if os.path.isfile(wpaper):
        os.remove(wpaper)
    shutil.copyfile(nwpaper,wpaper)
    os.system(cmd + wpaper)

def main():
    if len(sys.argv)==1:
        print 'Error: argument required.'
    else:
        wpchange(sys.argv[1])

if __name__ == '__main__':
    main()
