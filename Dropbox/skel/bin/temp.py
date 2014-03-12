#!/usr/bin/env python
#$Id: temp  08-05-2011 06:15PM William J. MacLeod(wimac1@gmail.com) ver: 11.217.1837
import feedparser,re
zipcode ='48126'
metric = 0


f=feedparser.parse('http://rss.accuweather.com/rss/liveweather_rss.asp?metric=%s&locCode=%s'% (metric,zipcode))

ctemp = f['entries'][0]['title']

print re.sub(r'Currently:\s?','',ctemp)







