#!/usr/bin/perl -wl

    use strict;

    # Get the month using cal
    my @cal = `cal @ARGV`;

    my $date =  shift @cal;
       $date =~ s/^\s+//;
       $date =~ s/\s+$//;

    shift   @cal; # Ignore short day names
    pop     @cal; # Ignore blank row
    unshift @cal, 'Sun Mon Tue Wed Thu Fri Sat'; # Add days


    # Some simple Html formatting
    print '<html>';
    print '<head>';
    print '<center>';
    print '<table border="1">';

    print "\t<tr>\n\t\t<td colspan=\"7\">" .
          "<center>$date</center></td>\t\n</tr>";

    # Print each day as a <td> element
    for (@cal) {
        print "\t<tr>";
        my @days = split ' ';

        # Left or right pad short weeks
        if (@days < 7) {
            if ($days[0] == 1) {
                unshift @days, ('&nbsp;') x (7 -@days);
            }
            else {
                push    @days, ('&nbsp;') x (7 -@days);
            }
        }

        print "\t\t<td>$_</td>" for @days;
        print "\t</tr>";
    }

    print '</table>';
    print '</center>';
    print '</head>';
    print '</html>';
