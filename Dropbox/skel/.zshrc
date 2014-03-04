# $Id: .zshrc  07-25-2007 01:13PM wimac ver: 11.006.1813
# Last modified: 01-06-2011  06:13PM ubuntu
# zsh init file
#AndroidDev PATH
export PATH=${PATH}:/home/wimac/dev/AndroidSDK/tools:/home/wimac/dev/AndroidSDK/platform-tools


# welcome text
clear
#echo -e ""
#echo -ne "Today is "; date
#echo -e ""; cal ;
export LC_ALL=en_US.utf8
export LC_LANG=en_US.utf8
if [ -d ~/bin ] ; then
    PATH=/usr/sbin:/sbin:~/bin:/usr/local/bin:"${PATH}"
fi
# THINGS WE DON'T WANT
# the builtin pwd prints the symbolic link instead of the real directory
disable pwd
# global alias file
source ~/bin/todo_completion
test -f ~/.aliasrc && source ~/.aliasrc
test -f ~/.zfunc && source ~/.zfunc
xmodmap ~/.Xmodmap
#fpath=(~/.zsh/functions $fpath)

cdpath=(.. ~ )  # specify a search path for the cd command.
#functions
find_alternatives(){ for i;do which "$i" >/dev/null && { echo "$i"; return 0;};done;return 1;}


# autoloads
autoload -U compinit
compinit

limit coredumpsize 0
autoload zsh-mime-setup; zsh-mime-setup
autoload zsh-mime-handler
# Environment variables
export BROWSER=$(find_alternatives chromium-browser google-chrome opera firefox firefox-bin iceweasel konqueror w3m lynx)
export EDITOR=$(find_alternatives vim nano pico emacs kate)
export PAGER=$(find_alternatives vimpager less most more pg)
export DISPLAY=:0
# only uncomment this if you have a recent version of keychain installed.
#keychain --quiet ~/.ssh/id_rsa ~/.ssh/id_dsa ~/.ssh/identity
#. ~/.keychain/${HOSTNAME}-sh

# Prompt 
PROMPT='[%n@%m] %# '
RPROMPT=' %~'     # prompt for right side of screen


# history settings
HISTFILE="$HOME/.zshhistory"
SAVEHIST=100000
HISTFILESIZE=100000000
HISTSIZE=100000
DIRSTACKSIZE=20




# Other misc settings
zstyle ':completion:*::::' completer _expand _complete _ignored _approximate

# allow one error for every three characters typed in approximate completer
zstyle -e ':completion:*:approximate:*' max-errors \
    'reply=( $(( ($#PREFIX+$#SUFFIX)/3 )) numeric )'
    
# insert all expansions for expand completer
zstyle ':completion:*:expand:*' tag-order all-expansions

# formatting and messages
zstyle ':completion:*' verbose yes
zstyle ':completion:*:descriptions' format '%B%d%b'
zstyle ':completion:*:messages' format '%d'
zstyle ':completion:*:warnings' format 'No matches for: %d'
zstyle ':completion:*:corrections' format '%B%d (errors: %e)%b'
zstyle ':completion:*' group-name ''

# match uppercase from lowercase
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# offer indexes before parameters in subscripts
zstyle ':completion:*:*:-subscript-:*' tag-order indexes parameters

# command for process lists, the local web server details and host completion
#zstyle ':completion:*:processes' command 'ps -o pid,s,nice,stime,args'
#zstyle ':completion:*:urls' local 'www' '/var/www/htdocs' 'public_html'
test -f $HOME/.hosts && hosts=(`cat $HOME/.hosts`)
zstyle '*' hosts $hosts

# Filename suffixes to ignore during completion (except after rm command)
zstyle ':completion:*:*:(^rm):*:*files' ignored-patterns '*?.o' '*?.c~' \
    '*?.old' '*?.pro'
# the same for old style completion
#fignore=(.o .c~ .old .pro)

# ignore completion functions (until the _ignored completer)
zstyle ':completion:*:functions' ignored-patterns '_*'

# OPTIONS
setopt appendhistory	# append to the zsh history file
setopt autocd		# go to a directory if first word on command line
setopt autoresume	# single-word commands may resume a suspended job
setopt cdablevars	# allows cd'ing to a parameter
setopt correct		# try to correct the spelling of commands
setopt csh_junkie_loops	# allow short form of loops: list; end
setopt extendedglob	# allow # and ^ to be used for filename generation
setopt globdots		# don't require leading . in filename to be matched
setopt histignoredups	# don't store duplicate lines in command history
setopt histnostore	# don't store history commands in history
setopt ignoreeof	# don't logout using Control-D
setopt longlistjobs	# list jobs in long format by default
setopt markdirs		# append trailing / to dirnames
setopt menucomplete	# cycle through completions when ambiguous
#setopt menucompletebeep	# beep on ambiguous completion
setopt numeric_globsort	# sort numeric filenames numerically
setopt noclobber	# don't overwrite existing files
setopt notify		# tell me when a job finishes
setopt rcquotes		# '' = single quote in single-quoted strings
unsetopt bgnice		# don't run background jobs at lower priority


copy-to-clipboard ()
{
  if [ -n "$LBUFFER$RBUFFER" ]; then
    echo $LBUFFER$RBUFFER | xclip -i
  fi
}

paste-from-clipboard ()
{
  CLIPOUT=`xclip -o`
  BUFFER=$LBUFFER$CLIPOUT$RBUFFER
}

zle -N paste-from-clipboard paste-from-clipboard
zle -N copy-to-clipboard copy-to-clipboard
bindkey "^V" paste-from-clipboard
bindkey "^Y" copy-to-clipboard

function precmd {

    local TERMWIDTH
    (( TERMWIDTH = ${COLUMNS} - 1 ))


    ###
    # Truncate the path if it's too long.
    
    PR_FILLBAR=""
    PR_PWDLEN=""
    
    local promptsize=${#${(%):---(%n@%m:%l)---()--}}
    local pwdsize=${#${(%):-%~}}
    
    if [[ "$promptsize + $pwdsize" -gt $TERMWIDTH ]]; then
	    ((PR_PWDLEN=$TERMWIDTH - $promptsize))
    else
	PR_FILLBAR="\${(l.(($TERMWIDTH - ($promptsize + $pwdsize)))..${PR_HBAR}.)}"
    fi


    ###
    # Get APM info.

#    if which ibam > /dev/null; then
#	PR_APM_RESULT=`ibam --percentbattery`
#    elif which apm > /dev/null; then
#	PR_APM_RESULT=`apm`
#    fi
}


setopt extended_glob
preexec () {
    if [[ "$TERM" == "screen" ]]; then
	local CMD=${1[(wr)^(*=*|sudo|-*)]}
	echo -n "\ek$CMD\e\\"
    fi
}


#setprompt () {
    ###
    # Need this so the prompt will work.

#    setopt prompt_subst


    ###
    # See if we can use colors.

#   autoload colors zsh/terminfo
#   if [[ "$terminfo[colors]" -ge 8 ]]; then
#colors
#   fi
#   for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
#eval PR_$color='%{$terminfo[bold]$fg[${(L)color}]%}'
#eval PR_LIGHT_$color='%{$fg[${(L)color}]%}'
#(( count = $count + 1 ))
#    done
#    PR_NO_COLOUR="%{$terminfo[sgr0]%}"
#

    ###
    # See if we can use extended characters to look nicer.
    
#    typeset -A altchar
#    set -A altchar ${(s..)terminfo[acsc]}
#    PR_SET_CHARSET="%{$terminfo[enacs]%}"
#    PR_SHIFT_IN="%{$terminfo[smacs]%}"
#    PR_SHIFT_OUT="%{$terminfo[rmacs]%}"
#    PR_HBAR=${altchar[q]:--}
#    PR_ULCORNER=${altchar[l]:--}
#    PR_LLCORNER=${altchar[m]:--}
#    PR_LRCORNER=${altchar[j]:--}
#    PR_URCORNER=${altchar[k]:--}
#
    
    ###
    # Decide if we need to set titlebar text.
    
#   case $TERM in
#	xterm*)
#	    PR_TITLEBAR=$'%{\e]0;%(!.-=*[ROOT]*=- | .)%n@%m:%~ | ${COLUMNS}x${LINES} | %y\a%}'
#	    ;;
#	screen)
#	    PR_TITLEBAR=$'%{\e_screen \005 (\005t) | %(!.-=[ROOT]=- | .)%n@%m:%~ | ${COLUMNS}x${LINES} | %y\e\\%}'
#	    ;;
#	*)
#	    PR_TITLEBAR=''
#	    ;;
#    esac
    
    
    ###
    # Decide whether to set a screen title
#    if [[ "$TERM" == "screen" ]]; then
#	PR_STITLE=$'%{\ekzsh\e\\%}'
##    else
#	PR_STITLE=''
#    fi
#    
    
    ###
    # APM detection
    
#    if which ibam > /dev/null; then
#	PR_APM='$PR_RED${${PR_APM_RESULT[(f)1]}[(w)-2]}%%(${${PR_APM_RESULT[(f)3]}[(w)-1]})$PR_LIGHT_BLUE:'
#    elif which apm > /dev/null; then
#	PR_APM='$PR_RED${PR_APM_RESULT[(w)5,(w)6]/\% /%%}$PR_LIGHT_BLUE:'
#    else
#	PR_APM=''
#    fi
    
    
    ###
    # Finally, the prompt.

#    PROMPT='$PR_SET_CHARSET$PR_STITLE${(e)PR_TITLEBAR}\
#$PR_CYAN$PR_SHIFT_IN$PR_ULCORNER$PR_BLUE$PR_HBAR$PR_SHIFT_OUT(\
#$PR_GREEN%(!.%SROOT%s.%n)$PR_GREEN@%m:%l\
#$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_CYAN$PR_HBAR${(e)PR_FILLBAR}$PR_BLUE$PR_HBAR$PR_SHIFT_OUT(\
#$PR_MAGENTA%$PR_PWDLEN<...<%~%<<\
#$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_CYAN$PR_URCORNER$PR_SHIFT_OUT\
#
#$PR_CYAN$PR_SHIFT_IN$PR_LLCORNER$PR_BLUE$PR_HBAR$PR_SHIFT_OUT(\
#%(?..$PR_LIGHT_RED%?$PR_BLUE:)\
#$PR_YELLOW%D{%H:%M}\
#$PR_LIGHT_BLUE:%(!.$PR_RED.$PR_WHITE)%#$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
#$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
#$PR_NO_COLOUR '
#
#    RPROMPT=' $PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_BLUE$PR_HBAR$PR_SHIFT_OUT\
#($PR_YELLOW%D{%a,%b%d}$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_CYAN$PR_LRCORNER$PR_SHIFT_OUT$PR_NO_COLOUR'

#    PS2='$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
#PR_BLUE$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT(\
#PR_LIGHT_GREEN%_$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
#PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT$PR_NO_COLOUR '

#setprompt

