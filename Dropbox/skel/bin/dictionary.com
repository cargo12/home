#!/bin/bash

# BASH script created by Ludootje <ludootje at linux dot be>
# written on: 09/08/2004 (Belgian date format)
# released under the GNU General Public License (a.k.a. GPL)
# original csh version written by Mark "mcangeli" Angeli

help() {
        echo "Usage:"
        echo "  --help: display this help."
        echo "  $0 word1 [word2 word3 ... wordn]"
        echo
        echo "You can use as many words as you like."
        echo "When you've read the explanation of the word, hit 'q' to move on to the next word."
        echo "To exit the program when it's running, hit ^C (i.e. control+c), followed by 'q'."

        exit 0
}

dict() {
       for i in "$@"; do
               lynx -dump "http://www.dictionary.com/cgi-bin/dict.pl?term=$i" | less
       done
       exit 0
}

case $1 in
   --help) help
      ;;
   *) for i in "$@"; do
         lynx -dump "http://www.dictionary.com/cgi-bin/dict.pl?term=$i" | less
    done
        exit 0
esac
#EOF
