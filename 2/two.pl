#!/usr/bin/env perl

use strict;
use warnings;

my %play_scores = (
  'A' => 1,
  'B' => 2,
  'C' => 3,
);

my %win_versus = (
  # rock vs sciss
  'A' => 'C',
  # paper vs rock
  'B' => 'A',
  # sciss vs paper
  'C' => 'B',
);

my %lose_versus = (
  # rock vs paper
  'A' => 'B',
  # paper vs sciss
  'B' => 'C',
  # sciss vs rock
  'C' => 'A',
);

my $score = 0;

while (<>) {
  my ($opponent, $choice) = m/([A-C]) ([X-Z])/;
  my $me;
  if ($choice eq 'X') {
    # lose
    $me = $win_versus{$opponent};
  } elsif ($choice eq 'Y') {
    # draw
    $score += 3;
    $me = $opponent;
  } else {
    # win
    $score += 6;
    $me = $lose_versus{$opponent};
  }
  $score += $play_scores{$me}; 
}

print "Score: $score\n";
