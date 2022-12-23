#!/usr/bin/env python3

from collections import defaultdict
from typing import Optional


def do_one_sand(sparse_grid: dict[int, dict[int, str]], max_y: int) -> tuple[bool, bool]:
  """
  Fills one sand, returning a tuple of False if the sand passed max_y (problem
  1), and False if the sand stopped at the source (problem 2).
  """
  sand_x, sand_y = 500, 0
  has_next = True
  while has_next:
    next_coords = do_one_sand_tick(sparse_grid, sand_x, sand_y, max_y)
    # Stopped!
    if next_coords == (sand_x, sand_y):
      return sand_y <= max_y, next_coords != (500, 0)
    sand_x, sand_y = next_coords


  assert False, "reached end of function prematurely"


def do_one_sand_tick(sparse_grid: dict[int, dict[int, str]], sand_x: int, sand_y: int, max_y: int) -> tuple[int, int]:
  """
  Does a single tick of sand, returning the next coordinate of the sand, or
  the input coordinates if the sand has stopped.
  """
  # Always down.
  next_y = sand_y + 1

  next_row = sparse_grid[next_y]

  # Try vertical, then left, then right.
  for try_x in (sand_x, sand_x - 1, sand_x + 1):
    if try_x not in next_row:
      if next_y <= max_y + 1:
        # Air.
        return try_x, next_y 
      # else is rock; continue.
    elif next_row[try_x] == ".":
      return try_x, next_y

  # Sand stuck. Mark grid, return.
  curr_row = sparse_grid[sand_y]
  assert curr_row.get(sand_x, ".") in ".+", f"bad row {curr_row} at y = {next_y}"
  curr_row[sand_x] = "O"
  # Sand is stuck.
  return sand_x, sand_y
  


def parse_coord(coord_pair: str) -> tuple[int, int]:
  splits = tuple(int(val) for val in coord_pair.split(","))
  assert len(splits), 2
  return splits


def print_grid(sparse_grid: dict[int, dict[int, str]], xrange: tuple[int, int], yrange: tuple[int, int]) -> None:
  for y in range(*yrange):
    for x in range(*xrange):
      print(sparse_grid[y].get(x, "."), end="")
      print(" ", end="")
    print()


def main():
  sparse_grid: dict[int, dict[int, str]] = defaultdict(dict)
  with open("input.txt", "r") as infile:
    for line in infile:
       line = line.strip("\n")
       coords = line.split(" -> ")
       assert len(coords) > 1
       curr_coord = parse_coord(coords[0])
       for next_coord_str in coords[1:]:
         next_coord = parse_coord(next_coord_str)
         if curr_coord[0] == next_coord[0]:
           assert curr_coord[1] != next_coord[1], f"bad coord on line {line}; curr={curr_coord}, next={next_coord}"
           # Vertical line.
           y_starts = sorted((curr_coord[1], next_coord[1]))
           for y in range(y_starts[0], y_starts[1] + 1):
             sparse_grid[y][curr_coord[0]] = "#"
         else:
           assert curr_coord[1] == next_coord[1]
           # Horizontal line.
           x_starts = sorted((curr_coord[0], next_coord[0]))
           for x in range(x_starts[0], x_starts[1] + 1):
             sparse_grid[curr_coord[1]][x] = "#"
         curr_coord = next_coord

  min_x = min(
    x for row in sparse_grid.values() for x in row.keys()
  )
  max_x = max(
    x for row in sparse_grid.values() for x in row.keys()
  )
  min_y = 0
  max_y = max(sparse_grid.keys())

  print(f"done. xrange - {min_x}, {max_x}. yrange - {min_y}, {max_y}")

  for y in range(min_y, max_y + 1):
    row = sparse_grid[y] 
    for x in range(min_x, max_x + 1):
      if x not in row:
        row[x] = "."
    assert len(row) == max_x - min_x + 1, f"row {y} has length {len(row)}; expected {max_x - min_x + 1}"
  assert len(sparse_grid) == max_y - min_y + 1
  # Start of my sand.
  sparse_grid[0][500] = "+"

  print("Starting grid -\n")
  print_grid(sparse_grid, (min_x, max_x + 1), (min_y, max_y + 1))

  counter = 0
  hit_floor_at = -1
  ended_at = -1
  while ended_at < 0:
    counter += 1 
    not_hit_floor, not_hit_top = do_one_sand(sparse_grid, max_y)
    if counter % 10 == 0:
      print(".", end="")

    if not not_hit_floor and hit_floor_at < 0:
      hit_floor_at = counter
    if not not_hit_top:
      ended_at = counter

  print("Ending grid -\n")
  print_grid(sparse_grid, (min_x, max_x + 1), (min_y, max_y + 2))

  print(f"done at sand {counter}.")
  print(f"{hit_floor_at} hit the floor (P1 answer = {hit_floor_at - 1}).")
  print(f"{ended_at} hit the ceiling (P2 answer = {ended_at}).")


if __name__ == '__main__':
    main()
