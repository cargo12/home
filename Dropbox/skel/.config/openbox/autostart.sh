TZ='America/Detroit'; export TZ&
export OOO_FORCE_DESKTOP=gnome
setxkbmap us &
setxkbmap -option ctrl:nocaps &
xmodmap -e "remove lock = Caps_Lock"
rm ~/lpriv
thunar --daemon &
(sleep 1 && $HOME/bin/wallpaper_changer) &
(sleep 1 && guake -e 'tmux_project') &
(sleep 1 && trayer --expand false --transparent true --widthtype request --alpha 255 --align center --SetDockType false) &
(sleep 2 && xfce4-power-manager) &
#(sleep 3 && keepassx) &
(sleep 4 && nm-applet) &
(sleep 4 && wjmRadioTray.py) &
(sleep 6 && $HOME/.dropbox-dist/dropboxd) &
(sleep 6 && $HOME/bin/conky_startup) &
#(sleep 6 && if [-d /home/media/wimac-drive/ ]; then $HOME/bin/ted.sh; fi) & 
(sleep 7 && xscreensaver -nosplash) &
(sleep 7 && flexget execute) &
(sleep 10 && transmission) &
# Disable Nautilus desktop, because we really really do not want it!
gconftool-2 -s -t bool /apps/nautilus/preferences/show_desktop false &
# Do not let Nautilus set the background, because we really really do not want this either.
gconftool-2 -s -t bool /desktop/gnome/background/draw_background false &
# Make Nautilus use spatial mode, should start-up quicker.
gconftool-2 -s -t bool /apps/nautilus/preferences/always_use_browser false &
# Make Nautilus show the advanced permissions dialog -- if it has to start, lets at least make it usable :) 
gconftool-2 -s -t bool /apps/nautilus/preferences/show_advanced_permissions true &
touch_kill &
mount /dev/sdb5 &
