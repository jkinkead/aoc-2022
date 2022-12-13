#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
import math
from typing import Callable, Optional


@dataclass
class Op:
  op: str = ""
  rhs: int = -1

  def apply(self, val) -> int:
    if self.op == "sq":
      return val * val 
    
    if self.op == "*":
      return val * self.rhs

    assert self.op == "+"
    return val + self.rhs


@dataclass
class Monkey:
  throws: int = 0
  # Items; value is worry level.
  items: list[int] = field(default_factory=list)
  operation: Optional[Op] = None
  divisible_by: int = 0
  true_target: int = -1
  false_target: int = -1
  max_mod: Optional[int] = None

  def take_turn(self, monkeys: list["Monkey"]) -> None:
    """
    Looks at all items, following The Rules.
    """
    for item in self.items:
      # Do operation.
      item = self.operation.apply(item)

      # Decrease worry by 1/3rd.
      # TODO: This is only part 2.
      # item = math.floor(item / 3)

      # Do test.
      if (item % self.divisible_by) == 0:
        target = self.true_target
      else:
        target = self.false_target

      item = item % self.max_mod

      # Do throw.
      monkeys[target].items.append(item)
      self.throws += 1

    self.items.clear()


def main():
  monkeys = []
  monkey_pattern = re.compile(r"Monkey \d+:")
  items_pattern = re.compile(r"Starting items: (.*)$")
  operation_pattern = re.compile(r"Operation: new = ([^ ]+) (.) ([^ ]+)$")
  test_pattern = re.compile(r"Test: divisible by (\d+)$")
  throw_pattern = re.compile(r"If (true|false): throw to monkey (\d+)$")
  with open("input.txt", "r") as infile:
    has_more = True
    while has_more:
      monkey = Monkey()
      monkeys.append(monkey)

      # Monkey num line.
      line = infile.readline()
      assert monkey_pattern.search(line) is not None, f"bad monkey line: {line}"

      # Starting items.
      line = infile.readline()
      match = items_pattern.search(line)
      assert match is not None, f"bad items line: {line}"
      monkey.items = [int(item_str) for item_str in match.group(1).split(", ")]

      # Operation.
      line = infile.readline()
      match = operation_pattern.search(line)
      assert match is not None, f"bad operation line: {line}"
      lhs, op, rhs = match.group(1, 2, 3)
      assert lhs == "old", f"can't handle {line}"
      if rhs == "old\n":
        assert op == "*"
        monkey.operation = Op(op="sq")
      else:
        rhs = int(rhs)
        if op == "*":
          monkey.operation = Op(op=op, rhs=rhs)
        else:
          assert op == "+", f"bad op on: {line}"
          monkey.operation = Op(op=op, rhs=rhs)

      # Test.
      line = infile.readline()
      match = test_pattern.search(line)
      assert match is not None, f"bad test line: {line}"
      monkey.divisible_by = int(match.group(1))

      # True line.
      line = infile.readline()
      match = throw_pattern.search(line)
      assert match is not None, f"bad throw line: {line}"
      assert match.group(1) == "true", f"bad true line: {line}"
      monkey.true_target = int(match.group(2))

      # False line.
      line = infile.readline()
      match = throw_pattern.search(line)
      assert match is not None, f"bad throw line: {line}"
      assert match.group(1) == "false", f"bad false line: {line}"

      monkey.false_target = int(match.group(2))

      # Blank line.
      line = infile.readline()
      has_more = line != ""

  max_mod = 1
  for mon in monkeys:
    max_mod = max_mod * mon.divisible_by
  for mon in monkeys:
    mon.max_mod = max_mod

  # Iterate 20 rounds.
  for i in range(0, 10000):
    for monkey in monkeys:
      monkey.take_turn(monkeys)


  # Find top-two monkeys.
  sorted_mons = sorted(monkeys, key=lambda mon: mon.throws)
  top_two = sorted_mons[-2:]

  # Monkey business: Throws for these two, multiplied together.
  business_value = top_two[0].throws * top_two[1].throws

  print(f"business time: {business_value}")



if __name__ == '__main__':
    main()
