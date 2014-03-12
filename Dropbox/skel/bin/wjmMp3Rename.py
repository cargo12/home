#!/usr/bin/env python
#
# Last modified: 09-06-2011  04:04PM crunchbang
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
#
# renames mp3 files in directory using ID3 tags to Artist Album Title.

__author__= "William J. MacLeod"
__email__="wimac1@gmail.com"
__license__="GPL"


import os,glob,eyeD3

path = ''
debug = 1

def getId3Tags(file):
    if debug == 1:
        print "processing" + file
    trackInfo = eyeD3.Mp3AudioFile(file)
    tag = trackInfo.getTag()
    #tag.link(file)
    artist=tag.getArtist()
    artist=artist.replace(' ','_')
    artist=artist.replace('?','')
    album=tag.getAlbum()
    album=album.replace(' ','_')
    album=album.replace('?','')
    title=tag.getTitle()
    title=title.replace(' ','_')
    title=title.replace('?','')
    nfile=artist +"-"+ album + "-" + title + ".mp3"
    if debug == 1:
        print nfile
    os.rename(file,nfile)

for infile in glob.glob( os.path.join(path, '*.mp3') ):
    if debug == 1:
        print "current file is: " + infile
    getId3Tags(infile)

for infile in glob.glob( os.path.join(path, '*.m4a') ):
    if debug == 1:
        print "current file is: " + infile
    getId3Tags(infile)

