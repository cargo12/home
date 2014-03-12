#!/bin/bash
# $Id: fitweather  07-26-2007 02:17PM wimac ver: 09.289.2305
# by William J. MacLeod (wimac1@gmail.com)  
# Last modified: 10-16-2009  11:05PM wimac
wxurl="http://www.weather.com/outlook/health/fitness/weather/hrbyhr/48126?x=0&from=fitloc&y=0"
size=3
curl -s --connect-timeout 30 "${wxurl}" | \
  sed -n '/Begin CC/,/Updated /p' |\
  sed 's/<[^>]*>//g;s/^ [ ]*//g;s/^[ \t]*//;s/[ \t]*$//' | \
  sed '/^.\{35\}/d'  |\
  sed '/&nbsp;/ s/&nbsp;/ /g;/&deg;/ s/&deg;//g' |\
  sed '/^$/d' |\
  sed '1,11!d' |\
  uniq -u | \
  tr -d '\r' 
exit 0
