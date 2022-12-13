#!/usr/bin/env perl

use strict;
use warnings;

my $curr = 0;
my @all = ();

while (<>) {
  chomp;
  if (m/^\s*$/) {
    push @all, $curr;
    $curr = 0;
  } else {
    $curr += $_;
  }
}

@all = sort { $b - $a } @all;

print "most 3 = $all[0], $all[1], $all[2]\n";
