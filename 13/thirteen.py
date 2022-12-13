#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
import math
from typing import Callable, Optional
from functools import cmp_to_key


def check_order(first, second) -> Optional[bool]:
  if type(first) != type(second):
    if type(first) == list:
      assert type(second) == int
      second = [second]
    else:
      assert type(first) == int
      first = [first]

  if type(first) == int:
    if first < second:    
      return True
    elif first > second:
      return False
    else:
      return None

  assert type(first) == list and type(second) == list

  # Check each element. Must be list.
  for i in range(0, len(first)):
    if i >= len(second):
      return False

    answer = check_order(first[i], second[i])
    if answer is not None:
      return answer

  # Exhausted first list. Check length.
  if len(first) == len(second):
    # Equal!
    return None
  else:
    # In order! First is shorter.
    return True

def sort_order(first, second) -> int:
  if type(first) != type(second):
    if type(first) == list:
      assert type(second) == int
      second = [second]
    else:
      assert type(first) == int
      first = [first]

  if type(first) == int:
    if first < second:    
      return -1
    elif first > second:
      return 1
    else:
      return 0

  assert type(first) == list and type(second) == list

  # Check each element. Must be list.
  for i in range(0, len(first)):
    if i >= len(second):
      return 1

    answer = sort_order(first[i], second[i])
    if answer != 0:
      return answer

  # Exhausted first list. Check length.
  if len(first) == len(second):
    # Equal!
    return 0
  else:
    # In order! First is shorter.
    return -1


def main():
  pair_count = 0
  good_pairs = []
  all_lines = []
  with open("input.txt", "r") as infile:
    has_more = True
    while has_more:
      pair_count += 1
      first = eval(infile.readline())
      second = eval(infile.readline())
      assert type(first) == list
      assert type(second) == list
      all_lines.append(first)
      all_lines.append(second)

      # Blank line.
      line = infile.readline()
      has_more = line != ""

      # Compare.
      answer = check_order(first, second)
      if answer is True:
        good_pairs.append(pair_count)
      elif answer is False:
        pass
      else:
        print(f"Warning: Equal on line {pair_count}")

  total = sum(good_pairs)

  print(f"done: {pair_count}; total = {total}")

  all_lines.append([[2]])
  all_lines.append([[6]])
  sorted_lines = sorted(all_lines, key=cmp_to_key(sort_order))
  index_start = sorted_lines.index([[2]])
  index_end = sorted_lines.index([[6]])

  print(f"done sorted: ({index_start}, {index_end}); key = {(index_start + 1) * (index_end + 1)}")


if __name__ == '__main__':
    main()
