#!/usr/bin/perl -w

use strict;
use English qw( -no_match_vars );

my $pid;
my $dir     = shift(@ARGV) || '.';
my $program = "find";
my $home    = $ENV{'HOME'};

# This is a short example based on file.pl.
# It reads from find.

die "cannot fork: $!" unless defined($pid = open(KID, "-|"));

if ($pid) {    # parent
    while (<KID>) {
	chomp;
	next if m!$home/notebook/!;
	next unless -T "$_";
	my ($size, $mtime) = (stat "$_")[7, 9];
	open(FH, "$_") or die "$! on $_";

	print <<EOF;
Content-Length: $size
Last-Mtime: $mtime
Path-Name: $_

EOF
	print <FH>;
	close(FH);
    }
    close KID;
}
else {
    $EUID      = $UID;
    $EGID      = $GID;
    $ENV{PATH} = "/bin:/usr/bin";
    exec($program, "$dir", '-type', 'f', '-print')
	or die "can't exec $program: $!";
}

exit(0);


