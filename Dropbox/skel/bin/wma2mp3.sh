##!/bin/bash

# Dump wma to mp3
# from http://ocaoimh.ie/2005/08/16/how-to-convert-from-wma-to-mp3/

for src in *.wma
do
  if [ -f "$src" ]
  then
    fifo=`echo "$src"|sed -e 's/wma$/wav/'`
    rm -f "$fifo"
    mkfifo "$fifo"
    mplayer -vo null -vc dummy -af resample=44100 -ao pcm:waveheader \
"$src" -ao pcm:file="$fifo" &
    dest=`echo "$src"|sed -e 's/wma$/mp3/'`
    lame --vbr-new "$fifo" "$dest"
    rm -f "$fifo"
  fi
done
