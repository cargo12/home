#!/bin/bash

#find . -iname \*.mp3 -print0 | xargs -0 mp3gain -krd 6 && vorbisgain -rfs .
find . - name '*.mp3' -exec mp3gain -r -k {} \;
