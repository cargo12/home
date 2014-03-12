#!/usr/bin/perl -w
use strict;

# This is a short example that basically does the same
# thing as the default file system access method.
# This will index only one directory.

my $dir = shift (@ARGV) || '.';
opendir D, $dir or die $!;
while ($_ = readdir D) {
    next unless -T "$dir/$_";
    my ($size, $mtime) = (stat "$dir/$_")[7, 9];
    open FH, "$dir/$_" or die "$! on $dir/$_";

    print <<EOF;
Content-Length: $size
Last-Mtime: $mtime
Path-Name: $dir/$_

EOF
    print <FH>;
    close FH;
}

exit(0);

