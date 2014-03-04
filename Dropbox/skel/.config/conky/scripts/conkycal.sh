#!/bin/bash
cd $(dirname $0)
# horizontal and vertical calendar for conky by ans
# Updated by: mobilediesel, dk75, Bruce, Crinos512, et al.
############################################################
# This work is licensed under the Creative Commons         #
# Attribution-Share Alike 3.0 Unported License.            #
# To view a copy of this license, visit                    #
# http://creativecommons.org/licenses/by-sa/3.0/           #
# or send a letter to Creative Commons, 171 Second Street, #
# Suite 300, San Francisco, California, 94105, USA.        #
############################################################
# locale depend week day names
# The 'lang' file must be in the same directory as this script.
# Horizontal and English are the defaults:
#     conkycal.sh
# Make it vertical:
#     conkycal.sh -v
# Change the language to Spanish:
#     conkycal.sh -l es
# Or both at once:
#     conkycal.sh -v -l es
# The order of the arguments doesn't matter:
#     conkycal.sh -l es -v
# Need to use a goto:
#     conkycal.sh -l es|sed 's/^/\${goto 240}/'
# or a goto and a tab:
#     conkycal.sh |sed -e 's/^/\${goto 240}/' -e 's/$/\${tab 20}/'
DOW=("Mo" "Tu" "We" "Th" "Fr" "Sa" "Su")
while getopts ":vl:" opts; do
case "$opts" in
l) lang=$OPTARG;;
v) orientation="$opts";;
esac
done
if [ -f lang ]; then
    . lang
fi
COLOROLD="667788" #MidSlateGrey
COLORTODAY="FFFFFF" #Darkorange
COLORREST="445566" #MidSlateGrey
COLORNEXT="778899" #LightSlateGrey
COLORSATURDAY="FF8C00"
COLORSUNDAY="FF8C00"
COLOR=("" "" "" "" "" "\${color $COLORSATURDAY}" "\${color $COLORSUNDAY}")
COLOREND=("" "" "" "" "" "" "\${color}")

TODAY=$(date +%-d)
LASTDAY=$(date -d "-$TODAY days +1 month" +%d)
FIRSTDAY=$(date -d "-$[$TODAY-1] days" +%u)

# horizontal function
h () {
# Build $TOPLINE
k=$FIRSTDAY
for j in {1..31}; do
  x=$[j+LASTDAY/j]
  case $j in
      ${j/#$x})    TOPLINE="$TOPLINE ${COLOR[$[k-1]]}${DOW[$[k-1]]}${COLOREND[$[k-1]]}";;
      $[LASTDAY+1])    TOPLINE="$TOPLINE \${color $COLORNEXT}${DOW[$[k-1]]}";;
      *)        TOPLINE="$TOPLINE ${DOW[$[k-1]]}";;
  esac
  k=$[${k/#7/0}+1]
done

BOTTOM="\${color $COLOROLD}$(seq -w -s ' ' $LASTDAY|sed "0,/[0-3]*$TODAY \?/s//\${color $COLORTODAY}&\${color $COLORREST}/") \${color $COLORNEXT}$(seq -w -s ' ' 0$[31-$LASTDAY])"

echo "${TOPLINE/# /}"
echo "$BOTTOM\${color}"
}

#vertical function
v () {
for i in $(seq 1 $[TODAY-1]); do
    TODAYC[$i]="\${color $COLOROLD}"
done
TODAYC[$TODAY]="\${color $COLORTODAY}"
for i in $(seq $[TODAY+1] $LASTDAY); do
    TODAYC[$i]="\${color $COLORREST}"
done

k=$FIRSTDAY
for j in $(seq $LASTDAY); do
      echo  "${COLOR[$[k-1]]}${DOW[$[k-1]]} ${TODAYC[$j]}$(printf "%02d" $j)\${color}"
  k=$[${k/#7/0}+1]
done
}

# call function based on "$orientation"
${orientation:-h}
