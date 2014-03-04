#!/bin/bash

# Location of unitinfo.txt
FAH="/opt/foldingathome/client1/unitinfo.txt"

if [ -f $FAH ]
  then
    sed -e 's/^Name:.\(.\{20\}\).*$/name = \1.../' -e 's/Progress:/progres/' -e 's/Due time:/due =/' -e 's/Download time:/downloaded =/'  -e '/^Current/d' -e '/^-/d' $FAH
fi

exit 0
