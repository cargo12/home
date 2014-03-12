#!/usr/bin/python
import sys, getopt, urllib, pwd, os

def main():
    output = ""
    verbose = False
    if len(sys.argv[1:]) < 1:
        NowPlaying()
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "c:tlagh", ["channel=", "track", "longname", "artist", "catagory"])
        except getopt.GetoptError:
            usage(verbose)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-c", "--channel"):
                channel = arg
                output += channel
            if opt in ("-t", "--track"):
                output += " " + getTrack(channel)
            if opt in ("-l", "--longname"):
                output += " " + getLongname(channel)
            if opt in ("-a", "--artist"):
                output += " " + getArtist(channel)
            if opt in ("-g", "--catagory"):
                output += " " + getCatagory(channel)
            if opt == "-h":
                verbose = True
                usage(verbose)
                sys.exit()
        print output

def getArtist(channel):
    output = ""
    importUrl = urllib.urlopen('http://sirius.criffield.net/' + channel + '/artist')
    for line in importUrl.readlines():
        output = line
    importUrl.close()
    return output

def getTrack(channel):
    output = ""
    importUrl = urllib.urlopen('http://sirius.criffield.net/' + channel + '/track')
    for line in importUrl.readlines():
        output = line
    importUrl.close()
    return output

def getLongname(channel):
    output = ""
    importUrl = urllib.urlopen('http://sirius.criffield.net/' + channel + '/longname')
    for line in importUrl.readlines():
        output = line
    importUrl.close()
    return output

def getCatagory(channel):
    output = ""
    importUrl = urllib.urlopen('http://sirius.criffield.net/' + channel + '/catagory')
    for line in importUrl.readlines():
        output = line
    importUrl.close()
    return output

def NowPlaying():
	playList = pwd.getpwuid(os.geteuid())[5] + "/.sipie/playlist"
	logStart = 15
	placeHolder = 0
	output = ""

	# Grab log[], hard coded to 1 line for now
	logFile = open(playList)
	output = logFile.readlines()[-1:]
	logFile.close

	# Assign values as needed
	placeHolder = find(output[0], ":", logStart)
	longname = toCapital(output[0][logStart:placeHolder]).strip()
	logStart = placeHolder + 2
	placeHolder = find(output[0], "-", logStart)
	artist = toCapital(output[0][logStart:placeHolder]).strip()
	logStart = placeHolder + 1
	track = toCapital(output[0][logStart:len(output[0])]).strip()

	#output[0] = "%B%C09Now Playing%O on %C07" + station + "%O: %C00" + artist + "%O - %C08" + title
	print longname + ": " + artist + "\n" + track
    #sys.exit()

def find(strng, ch, start):
    index = start 
    while index < len(strng):
        if strng[index] == ch:
            return index
        index = index + 1
    return -1

def findChar(strng, ch):
	return find(strng, ch, 0)

def toCapital(strng):
    return strng[0:1].upper() + strng[1:len(strng)]

def usage(verbose):
    if verbose == False:
        print """This is a test print"""
    else:
        print "arg.py [-c][-t][-l][-a]\nArgs: " + str(sys.argv[1:])

if __name__ == "__main__":
    main()
