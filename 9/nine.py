#!/usr/bin/env python3

import re
from dataclasses import dataclass, field

@dataclass
class Pos:
  head_x:int = 0
  head_y:int = 0
  tail_x:int = 0
  tail_y:int = 0

@dataclass
class BigPos:
  xs: list[int] = field(default_factory=list)
  ys: list[int] = field(default_factory=list)

  def move(self, direction: str):
    # Move head.
    if direction == 'U':
      self.ys[0] -= 1
    elif direction == 'D':
      self.ys[0] += 1
    elif direction == 'L':
      self.xs[0] -= 1
    elif direction == 'R':
      self.xs[0] += 1
    else:
      assert False, f"bad: {direction}"

    # Reconcile the rest.
    for i in range(0, 9):
      self.reconcile(i, i + 1)

  def reconcile(self, head_i, tail_i):
    # Move tail, if needed.
    if abs(self.xs[head_i] - self.xs[tail_i]) > 1 or abs(self.ys[head_i] - self.ys[tail_i]) > 1:
      # Need to move.

      # Vertical.
      if self.xs[head_i] == self.xs[tail_i]:
        if self.ys[head_i] > self.ys[tail_i]:
          self.ys[tail_i] += 1
        else:
          assert self.ys[head_i] < self.ys[tail_i]
          self.ys[tail_i] -= 1
      # Horizontal.
      elif self.ys[head_i] == self.ys[tail_i]:
        if self.xs[head_i] > self.xs[tail_i]:
          self.xs[tail_i] += 1
        else:
          assert self.xs[head_i] < self.xs[tail_i]
          self.xs[tail_i] -= 1
      else:
        # Diagonal.
        if self.xs[head_i] > self.xs[tail_i]:
          assert self.xs[head_i] > self.xs[tail_i]
          self.xs[tail_i] += 1
        else:
          assert self.xs[head_i] < self.xs[tail_i]
          self.xs[tail_i] -= 1
        if self.ys[head_i] > self.ys[tail_i]:
          assert self.ys[head_i] > self.ys[tail_i]
          self.ys[tail_i] += 1
        else:
          assert self.ys[head_i] < self.ys[tail_i]
          self.ys[tail_i] -= 1
    

def move(direction: str, pos: Pos):
  # Move head.
  if direction == 'U':
    pos.head_y -= 1
  elif direction == 'D':
    pos.head_y += 1
  elif direction == 'L':
    pos.head_x -= 1
  elif direction == 'R':
    pos.head_x += 1
  else:
    assert False, f"bad: {direction}"

  # Move tail, if needed.
  if abs(pos.head_x - pos.tail_x) > 1 or abs(pos.head_y - pos.tail_y) > 1:
    # Need to move.

    # Vertical.
    if pos.head_x == pos.tail_x:
      if pos.head_y > pos.tail_y:
        pos.tail_y += 1
      else:
        assert pos.head_y < pos.tail_y
        pos.tail_y -= 1
    # Horizontal.
    elif pos.head_y == pos.tail_y:
      if pos.head_x > pos.tail_x:
        pos.tail_x += 1
      else:
        assert pos.head_x < pos.tail_x
        pos.tail_x -= 1
    else:
      # Diagonal.
      if pos.head_x > pos.tail_x:
        assert pos.head_x > pos.tail_x
        pos.tail_x += 1
      else:
        assert pos.head_x < pos.tail_x
        pos.tail_x -= 1
      if pos.head_y > pos.tail_y:
        assert pos.head_y > pos.tail_y
        pos.tail_y += 1
      else:
        assert pos.head_y < pos.tail_y
        pos.tail_y -= 1


def main():
  visited: set[tuple[int, int]] = set()
  visited.add((0, 0))
  pos = Pos()
  big_pos = BigPos(
    xs=[0 for _ in range(0, 10)],
    ys=[0 for _ in range(0, 10)],
  )
  big_visited: set[tuple[int, int]] = set()
  big_visited.add((0, 0))
  move_pattern = re.compile(r"^([UDLR]) (\d+)$")
  with open("input.txt", "r") as infile:
    for line in infile:
      match = move_pattern.search(line)
      assert match is not None, f"bad line {line}"
      direction, count = match.group(1, 2)
      count = int(count)
      for _ in range(count):
        move(direction, pos)
        visited.add((pos.tail_x, pos.tail_y))
        big_pos.move(direction)
        big_visited.add((big_pos.xs[-1], big_pos.ys[-1]))

  print(f"tail visited {len(visited)} spaces")
  print(f"big tail visited {len(big_visited)} spaces")


if __name__ == '__main__':
    main()
