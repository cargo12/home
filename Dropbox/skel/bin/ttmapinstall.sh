#!/bin/bash
# ttmapinstall.sh by Stefan Tomanek <stefan@pico.ruhr.de>
# http://stefans.datenbruch.de/tomtom/
#
# Extracts and installs a Tomtom map archive on a Tomtom
# ONE or GO storage medium

INI="$1"
TARGET="$2"

if ! [ -e "$INI" ]; then
    echo "ini file not found!" >&2
    exit 1
fi

if [ ! -d "$TARGET"  -o ! -w "$TARGET" ]; then
    echo "target directory not writable!" >&2
    exit 1
fi

NAME=$(awk -F= '$1 == "Description" { gsub("\r", ""); print $2}' $INI)
echo "Now trying to install $NAME to $TARGET..." >&2

# Try to get cab file
MAPCAB=$(dirname $INI)/$(awk -F= '$1 ~ /^CabFiles */ { gsub("\r", ""); print $2}' $INI)

if ! [ -e "$MAPCAB" ]; then
    echo "cab file not found!" >&2
    echo "($MAPCAB)" >&2
    exit 1
fi

mkdir $TARGET/$NAME
cabextract -d "$TARGET/$NAME" "$MAPCAB"

cd $TARGET/$NAME

echo "Now renaming..." >&2
awk -F= '$1 ~ /^File[0-9]+$/ {
    gsub("\r", "");
    sub("File", "", $1);
    print $1, $2;
}' $INI | while read NUM FILE; do
    echo $(echo *.$NUM)" => $FILE" >&2
    mv *.$NUM $FILE
done
