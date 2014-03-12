#!/usr/bin/perl -w

# Simple script to burn MP3's to audiocd with Gtk-interface.
# This script converts MP3-files first to WAV-files
# with mpg123 and then it burns them to CD with cdrecord.
# Needs Perl::Gtk and MPEG::MP3Info packages from CPAN
# Copyright Henry Palonen <h@yty.net>, 2001
#
# Released under GPL

# CHANGES:
# 13.6.2001
# * Added support for mp3, MP3, mP3, Mp3 etc. files. Fix by Danial Pearce <danial@infoxchange.net.au>
# * Fixed a bug that caused program to exit when "filename.mp3" wasn't a true mp3-file.
# 17.4.2001
# * Added support for MPEG::MP3Info to get song-length
# FIXES:
# 17.4.2001
# * "spaces at directory name" bugfix by Ryan Hughes <Ryan.C.Hughes@colorado.edu>
# * reads both "*.MP3" and "*.mp3" files
# * fixed bug that appeared if there were spaces in subdirectory's name
# BUGS:
# * none at the moment

use Gtk;
use strict;
use MPEG::MP3Info;

init Gtk;
set_locale Gtk;

# Directory where MP3's are first looked
#my $root_dir = "/mp3";

my $root_dir = `pwd`;
chomp($root_dir);

# Directory where WAV files are stored. This should have
# enough free space...
my $burntmp="/mp3/burntmp";

# General settings for burn
my $speed = "4";
my $cdrdevice = "1,0,0";
my $cdrecord="/usr/bin/cdrecord";
my $cdoptions=" -v -audio -pad ";

# ----------- NO SETTINGS (shouldn't be) BELOW THIS LINE ------

my $false = 0;
my $true = 1;
my @titles;
my $window;
my $pane;
my $vbox;
my $tree_scrolled_win;
my $fromlist_scrolled_win;
my $entry;
my $tree;
my $leaf;
my $subtree;
my $item;
my $fromlist;
my $hbox1;
my $hbox2;
my $tolist;
my $vbox2;
my $vbox3;
my $btnadd;
my $btnremove;
my $btndone;
my $btnexit;
my $btnaddall;
my $btnbox;

$window = new Gtk::Window( 'toplevel' );
$window->set_usize( 725, 500 );
$window->set_title( "MP3 to CD-audio converter 0.1" );
$window->signal_connect( "delete_event", sub { Gtk->exit( 0 ); } );

$pane = new Gtk::HPaned();
$window->add( $pane );
$pane->set_handle_size( 10 );
$pane->set_gutter_size( 8 );
$pane->show();

$vbox = new Gtk::VBox( $false, 0 );
$pane->add1( $vbox );
$vbox->show();

$entry = new Gtk::Entry();
$vbox->pack_start( $entry, $false, $false, 4 );
$entry->signal_connect( 'activate', \&entry_activate );
$entry->show();

$tree_scrolled_win = new Gtk::ScrolledWindow( undef, undef );
$tree_scrolled_win->set_usize( 120, 400 );
$vbox->pack_start( $tree_scrolled_win, $true, $true, 0 );
$tree_scrolled_win->set_policy( 'automatic', 'automatic' );
$tree_scrolled_win->show();

$fromlist_scrolled_win = new Gtk::ScrolledWindow( undef, undef );
$pane->add2( $fromlist_scrolled_win );
$fromlist_scrolled_win->set_policy( 'automatic', 'automatic' );
$fromlist_scrolled_win->show();

$tree = new Gtk::Tree();
$tree_scrolled_win->add_with_viewport( $tree );
$tree->set_selection_mode( 'single' );
$tree->set_view_mode( 'item' );
$tree->show();

$leaf = new_with_label Gtk::TreeItem( $root_dir );
$tree->append( $leaf );
$leaf->signal_connect( 'select', \&select_item, $root_dir );
$leaf->set_user_data( $root_dir );
$leaf->show();

if ( has_sub_trees( $root_dir ) )
{
$subtree = new Gtk::Tree();
$leaf->set_subtree( $subtree );
$leaf->signal_connect( 'expand', \&expand_tree, $subtree );
$leaf->signal_connect( 'collapse', \&collapse_tree );
$leaf->expand();
}

$hbox1 = new Gtk::HBox( $false, 0 );
$fromlist_scrolled_win->add_with_viewport( $hbox1 );
$hbox1->show();

@titles = qw( Filename Size FullName);
$fromlist = new_with_titles Gtk::CList( @titles );
$hbox1->pack_start( $fromlist, $false, $false, 4 );
$fromlist->set_column_width( 0, 170 );
$fromlist->set_column_width( 1, 30 );
$fromlist->set_column_width( 2, 0 );
$fromlist->set_selection_mode( 'multiple' );
$fromlist->set_shadow_type( 'none' );
$fromlist->show();

$hbox2 = new Gtk::HBox( $false, 1 );
$hbox1->add( $hbox2 );
$hbox2->show();

$btnbox = new Gtk::VButtonBox();
$hbox2->add($btnbox);
$btnbox->show();

$btnadd = new Gtk::Button(">");
$btnbox->add($btnadd);
$btnadd->signal_connect( 'clicked', \&btnadd_click );
$btnadd->show();

$btnaddall = new Gtk::Button(">>");
$btnbox->add($btnaddall);
$btnaddall->signal_connect( 'clicked', \&btnaddall_click );
$btnaddall->show();

$btnremove = new Gtk::Button("<<");
$btnbox->add($btnremove);
$btnremove->signal_connect( 'clicked', \&btnremove_click );
$btnremove->show();

$btndone = new Gtk::Button("mp2wav2cd");
$btnbox->add($btndone);
$btndone->signal_connect( 'clicked', \&btndone_click );
$btndone->show();

$btnexit = new Gtk::Button("Exit");
$btnbox->add($btnexit);
$btnexit->signal_connect( 'clicked', sub { Gtk->exit( 0 ); } );
$btnexit->show();

@titles = qw( Filename Size FullName);
$tolist = new_with_titles Gtk::CList( @titles );
$hbox2->pack_start( $tolist, $false, $false, 4 );
$tolist->set_column_width( 0, 170 );
$tolist->set_column_width( 1, 30 );
$tolist->set_column_width( 2, 0 );
$tolist->set_selection_mode( 'single' );
$tolist->set_shadow_type( 'none' );
$tolist->show();

$window->show();
main Gtk;
exit( 0 );

##########################################
######### SUBROUTINES START HERE #########
##########################################

sub btnremove_click
{
	$tolist->clear();
}

sub btnaddall_click
{
my $row;
my $rowcount;
        $rowcount = $fromlist->rows;
        for ($row=0; $row<$rowcount;$row++)
        {
                $tolist->append (
			$fromlist->get_text($row,0),
			$fromlist->get_text($row,1),
			$fromlist->get_text($row,2)) ;
		$fromlist->unselect_all();
        }
}

sub btndone_click
{

	my @list;
	my $row;
	my $list;
	my $filename;
	my $size;
	my $fullname;
	my @mp3list;
	my $rowcount;
	my $order="";
	
	$rowcount = $tolist->rows;
	for ($row=0; $row<$rowcount;$row++)
	{
		$fullname = $tolist->get_text( $row, 2 );
		push(@mp3list, $fullname);
	}

	foreach my $mp3name (@mp3list)
	{
		my $mp3short = $mp3name;
		$mp3short =~ s|/.*/||g;
		$mp3short = "$burntmp/" . $mp3short . ".wav";
		`mpg123 -v -q -w \"$mp3short\" \"$mp3name\"\n`;
		print "\n-> $mp3short MP3->WAV OK\n";
		$order = $order . " \"$mp3short\" ";
	}

	for (my $i=5;$i>0;$i--) {
		print "-------- STARTING BURN IN $i SECONDS !!!! ------\n";
		sleep(1);
	}

	my $cmdline = "$cdoptions speed=$speed dev=$cdrdevice $order "; 

	# actual command that burns the CD goes here
	`$cdrecord $cmdline`;
	
	print "-------- END OF BURN ------\nREMOVING TEMP-FILES\n";
	`rm -fv $order`;
	print "-------- OK. END OF PROCESS.\n";
}

sub btnadd_click
{

	my @list;
	my $row;
	my $list;
	my $filename;
	my $size;
	my $fullname;

	@list = $fromlist->selection();
	foreach my $row (@list)
	{
		$filename = $fromlist->get_text( $row, 0 );
		$size = $fromlist->get_text( $row, 1 );
		$fullname = $fromlist->get_text( $row, 2 );
		$tolist->append($filename,$size,$fullname);
	}

	$fromlist->unselect_all();
}

sub expand_tree
{
	my ( $item, $subtree ) = @_;
	my $dir;
	my $dir_entry;
	my $path;
	my $item_new;
	my $new_subtree;

	$dir = $item->get_user_data();
	chdir( $dir );
	foreach $dir_entry ( <*> )

	  {
	    if ( -d $dir_entry )
	      {
		$path = $dir . "/" . $dir_entry;
		$path =~ s|//|/|g;
		$item_new = new_with_label Gtk::TreeItem( $dir_entry );
		$item_new->set_user_data( $path );
		$item_new->signal_connect( 'select', \&select_item, $path );
		$subtree->append( $item_new );
		$item_new->show();

		if ( has_sub_trees( $path ) )
		  {
		    $new_subtree = new Gtk::Tree();
		    $item_new->set_subtree( $new_subtree );
		    $item_new->signal_connect( 'expand',
					       \&expand_tree,
					       $new_subtree );
		    $item_new->signal_connect( 'collapse', \&collapse_tree );
		  }
	      }
	  }
	chdir( ".." );
}

sub collapse_tree
{
	my ( $item ) = @_;
	my $subtree = new Gtk::Tree();
	$item->remove_subtree();
	$item->set_subtree( $subtree );
	$item->signal_connect( 'expand', \&expand_tree, $subtree );
}

sub has_sub_trees
{
	my ( $dir ) = @_;
	my $file;
	foreach $file ( <"$dir"/*> )
	  {
	    return $true if ( -d $file );
	  }
	return ( $false );
}

sub select_item
{
	my ( $widget, $path ) = @_;
	$entry->set_text( $path );
	show_files( $path );
}

sub entry_activate
{
	my ( $entry ) = @_;
	my $path = $entry->get_text();
	if ( -d $path )
	  {
	    show_files( $path );
	  }
	else
	  {
	    $entry->set_text( "$root_dir" );
	  }
}

sub show_files
{
	my ( $path ) = @_;
	my $file;
	my $fullpath;
	my @files=();
	$fromlist->clear();

	opendir(DIR, $path) || die "can't open dir $path: $!";
	@files = grep { /\.mp3/i && -f "$path/$_" } readdir(DIR);
	closedir DIR;

	foreach $file (@files) 
	  {
	    unless ( -d $file )
	      {
		$fullpath = "$path/$file";
		my $time="";
		my $mp3info = new MP3::Info $file;
		if ($mp3info) { $time = $mp3info->time; }
		#$file =~ s|/ .*/||g;
		$file =~ s/\/.*\///g;
		# print "file: $file\n";
		$fromlist->append( $file, $time,$fullpath );
	      }
	  }    
}

# end of program
