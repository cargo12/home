#!/usr/bin/perl

#
# Copyright 2005-2006 Michal J. Kubski 
# Distributed under the terms of GNU General Public License v2
#

open OUTFILE, ">$ARGV[0]";

print OUTFILE "<openbox_menu>\n";

$find = `find /usr/share/applications /usr/share/gnome/apps -follow -type f -name "*.desktop" 2> /dev/null`;

@findLines = split("\n",$find);
foreach $fL (@findLines) {
    open DESKTOP, "<$fL";
    $category="";
    $exec="";
    $name="";
    $nameDe="";
    while (<DESKTOP>) {
	s/\n//g;
	if (/^Categories=/) {	    
	    $category = $_;
	    $category =~ s/\;/\//g;
	    $category =~ s/^Categories=//;
	} elsif (/^Exec=/) {	    
	    $exec = $_;
	    $exec =~ s/^Exec=//;
	} elsif (/^Name=/) {	    
	    $name = $_;
	    $name =~ s/^Name=//;
	} elsif (/^Name\[de\]=/) {	    
	    $nameDe = $_;
	    $nameDe =~ s/^Name\[de\]=//;
	}	
    }
    close DESKTOP;
    
    #xcdroast has no default Name so we take the Deutsch variant
    if ($name eq "") {
	$name = $nameDe;
    }
    $category =~ s/(GNOME|Qt|GTK|Application|Openbox|InstantMessaging)//g;
    $category =~ s/(AudioVideo|Audio\/Video|Player|DiscBurning)/Multimedia/g;
    $category =~ s/\/.*?Graphics/\/Graphics/g;
    $category =~ s/Multimedia(\/Multimedia)*/Multimedia/g;
    $category =~ s/Graphics(\/Graphics)*/Graphics/g;
    $category =~ s/(X-Red.*?|X-Su.*?)\///g;
    $category = "Applications/".$category;
    $category =~ s/\/(\/)*/\//g;
    $category =~ s/(^\/|\/$)//g;
    $exec =~ s/ \%.//g;
    $names2exec{$name} = $exec;
    $names2cats{$name} = $category;
    @k = split("/", $category);
    for (my $i=$#k; $i>=0; $i--) {
	$cats{join("/", @k)} = 1;
	pop @k;
    }
}

$last = -1;
$count = 0;
foreach my $cat (sort keys %cats) {
    my @r = split("/",$cat);
    my $clev = $#r; # here is current level of menu
    
    $lastPartCat = $r[$#r];    
    $id = "genid".($count++);
    if ($count == 1) {
	$id = "Applications"; #first item must match what we include from Main menu
    }

    $toclose = ($last - $clev) + 1; # count how many levels shall we close
    for (my $i=0; $i<$toclose; $i++) { # end close
	print OUTFILE "</menu>\n";
    }
    print OUTFILE "<menu id=\"$id\" label=\"$lastPartCat\">\n"; # open new menu
    foreach my $name (sort keys %names2cats) {
	my $cat1 = $names2cats{$name};
	my $exec = $names2exec{$name};
	if ($cat1 eq $cat) { # if item is in that menu, add it here
	    print OUTFILE "<item label=\"$name\"><action name=\"Execute\"><execute>$exec</execute></action></item>\n";
	}
    }
    $last = $clev;
}

$toclose = $last + 1; # count how many levels shall we close
for (my $i=0; $i<$toclose; $i++) { # end close
    print OUTFILE "</menu>\n";
}

print OUTFILE "</openbox_menu>\n";
close OUTFILE;