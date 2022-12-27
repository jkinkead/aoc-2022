#!/usr/bin/env python3

from dataclasses import dataclass, replace
from enum import Enum
import re


class OreType(Enum):
  ORE = 0
  CLAY = 1
  OBSIDIAN = 2
  GEODE = 3


@dataclass
class Blueprint:
  number: int
  ore_cost: int
  clay_cost: int
  obsidian_cost_ore: int
  obsidian_cost_clay: int
  geode_cost_ore: int
  geode_cost_obsidian: int


@dataclass
class State:
  blueprint: Blueprint

  ore_robot_count: int = 1
  clay_robot_count: int = 0
  obsidian_robot_count: int = 0
  geode_robot_count: int = 0

  ore_count: int = 0
  clay_count: int = 0
  obsidian_count: int = 0
  geode_count: int = 0

  minute: int = 0

  def better_than_or_equal(self, other: "State") -> bool:
    """Returns True if this is better than or equivalent to the given other state."""
    return (
      self.ore_robot_count >= other.ore_robot_count and self.clay_robot_count >= other.clay_robot_count and
      self.obsidian_robot_count >= other.obsidian_robot_count and self.geode_robot_count >= other.geode_robot_count and
      self.ore_count >= other.ore_count and self.clay_count >= other.clay_count and
      self.obsidian_count >= other.obsidian_count and self.geode_count >= other.geode_count
    )

  def better_sort_key(self, total_minutes) -> tuple[int, int, int, int]:
    minutes_left = total_minutes - self.minute
    ore_score = (
      self.ore_count + self.ore_robot_count * minutes_left +
      self.ore_robot_count * self.blueprint.ore_cost +
      self.clay_robot_count * self.blueprint.clay_cost +
      self.obsidian_robot_count * self.blueprint.obsidian_cost_ore +
      self.geode_robot_count * self.blueprint.geode_cost_ore
    )
    clay_score = (
      self.clay_count + self.clay_robot_count * minutes_left +
      self.obsidian_robot_count * self.blueprint.obsidian_cost_clay
    )
    obsidian_score = (
      self.obsidian_count + self.obsidian_robot_count * minutes_left +
      self.geode_robot_count * self.blueprint.geode_cost_obsidian
    )
    geode_score = self.geode_count + self.geode_robot_count * minutes_left
    return (geode_score, obsidian_score, clay_score, ore_score)

  def score(self, total_minutes) -> int:
    minutes_left = total_minutes - self.minute
    return self.geode_count + self.geode_robot_count * minutes_left + sum(range(0, minutes_left))

  def key(self) -> tuple[int, int, int, int, int, int, int, int]:
    return (self.geode_robot_count, self.geode_count, self.obsidian_robot_count, self.obsidian_count, self.clay_robot_count, self.clay_count, self.ore_robot_count, self.ore_count)

  def sort_key(self) -> tuple[int, int, int, int, int, int, int, int, int]:
    return (self.geode_robot_count, self.obsidian_robot_count, self.clay_robot_count, self.clay_count, -self.minute, self.geode_count, self.obsidian_count, self.ore_robot_count, self.ore_count)

  def clone(self) -> "State":
    return State(
      blueprint=self.blueprint,
      ore_robot_count=self.ore_robot_count,
      clay_robot_count=self.clay_robot_count,
      obsidian_robot_count=self.obsidian_robot_count,
      geode_robot_count=self.geode_robot_count,
      ore_count=self.ore_count,
      clay_count=self.clay_count,
      obsidian_count=self.obsidian_count,
      geode_count=self.geode_count,
      minute=self.minute,
    )

  def can_build_robots(self, robots_to_build: list[OreType]) -> bool:
    ore_count = self.ore_count
    clay_count = self.clay_count
    obsidian_count = self.obsidian_count
    for robot in robots_to_build:
      if robot == OreType.ORE:
        ore_count -= self.blueprint.ore_cost
      elif robot == OreType.CLAY:
        ore_count -= self.blueprint.clay_cost
      elif robot == OreType.OBSIDIAN:
        ore_count -= self.blueprint.obsidian_cost_ore
        clay_count -= self.blueprint.obsidian_cost_clay
      else:
        ore_count -= self.blueprint.geode_cost_ore
        obsidian_count -= self.blueprint.geode_cost_obsidian

    return ore_count >= 0 and clay_count >= 0 and obsidian_count >= 0

  def tick(self, robots_to_build: list[OreType]):
    # Ensure we can build robot (commit resources).
    for robot in robots_to_build:
      if robot == OreType.ORE:
        self.ore_count -= self.blueprint.ore_cost
        assert self.ore_count >= 0
      elif robot == OreType.CLAY:
        self.ore_count -= self.blueprint.clay_cost
        assert self.ore_count >= 0
      elif robot == OreType.OBSIDIAN:
        self.ore_count -= self.blueprint.obsidian_cost_ore
        assert self.ore_count >= 0
        self.clay_count -= self.blueprint.obsidian_cost_clay
        assert self.clay_count >= 0
      else:
        assert robot == OreType.GEODE
        self.ore_count -= self.blueprint.geode_cost_ore
        assert self.ore_count >= 0
        self.obsidian_count -= self.blueprint.geode_cost_obsidian
        assert self.obsidian_count >= 0

    # Harvest.
    self.ore_count += self.ore_robot_count
    self.clay_count += self.clay_robot_count
    self.obsidian_count += self.obsidian_robot_count
    self.geode_count += self.geode_robot_count

    # Actually build the robot.
    for robot in robots_to_build:
      if robot == OreType.ORE:
        self.ore_robot_count += 1
      elif robot == OreType.CLAY:
        self.clay_robot_count += 1
      elif robot == OreType.OBSIDIAN:
        self.obsidian_robot_count += 1
      else:
        self.geode_robot_count += 1

    # Increment minute.
    self.minute += 1


def simulate(blueprints, minutes):
  # Simulate for 24 minutes, for each blueprint.
  print(f"blueprints = {blueprints}")
  best_geodes_by_blueprint_number: dict[int, int] = {}
  for blueprint in blueprints:
    state_frontier = [State(blueprint=blueprint)]
    visited_minute = {}
    print(f"starting blueprint {blueprint.number}...")
    best_geodes_by_blueprint_number[blueprint.number] = 0

    count = 0
    while state_frontier:
      if count % 100000 == 0 and count > 0:
        print(f"at {count}, frontier length = {len(state_frontier)}, blueprint {blueprint.number}, best = {best_geodes_by_blueprint_number}, seen {len(visited_minute)} states ...")
      count += 1
      curr_state = state_frontier.pop()
      key = curr_state.key()
      if key in visited_minute:
        if visited_minute[key] >= curr_state.better_sort_key(minutes):
          continue

      visited_minute[key] = curr_state.better_sort_key(minutes)
     
      if curr_state.score(minutes) < best_geodes_by_blueprint_number[blueprint.number]:
        continue

      if curr_state.minute == minutes:
        # At the end! Save.
        best_so_far = best_geodes_by_blueprint_number.get(blueprint.number, 0)
        best_geodes_by_blueprint_number[blueprint.number] = max(curr_state.geode_count, best_so_far)
      else:
        assert curr_state.minute < minutes

        # Pick possible next actions.
        if curr_state.can_build_robots([OreType.GEODE]):
          next_move_frontier = [[OreType.GEODE]]
        else:
          next_move_frontier = [
            [OreType.ORE],
            [OreType.CLAY],
            [OreType.OBSIDIAN],
          ]
          if (
            not curr_state.can_build_robots(next_move_frontier[0]) or
            not curr_state.can_build_robots(next_move_frontier[1]) or
            not curr_state.can_build_robots(next_move_frontier[2])
          ):
            # Only explore a no-op if there's at least one robot type we can't build.
            # Otherwise, we're not saving for anything!
            next_move_frontier.append([])

        for next_move in next_move_frontier:
          if curr_state.can_build_robots(next_move):
            next_state = curr_state.clone()
            next_state.tick(next_move)
            state_frontier.append(next_state)

        if count % 10000 == 0:
          state_frontier.sort(key=lambda state: state.better_sort_key(minutes))
  return best_geodes_by_blueprint_number
    

def main():
  blueprints = []
  blueprint_pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.")
  with open("input.txt", "r") as infile:
    for line in infile:
      match = blueprint_pattern.search(line)    
      assert match is not None
      number, ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = match.group(1, 2, 3, 4, 5, 6, 7)
      blueprints.append(Blueprint(
          number=int(number),
          ore_cost=int(ore_cost),
          clay_cost=int(clay_cost),
          obsidian_cost_ore=int(obsidian_cost_ore),
          obsidian_cost_clay=int(obsidian_cost_clay),
          geode_cost_ore=int(geode_cost_ore),
          geode_cost_obsidian=int(geode_cost_obsidian),
      ))

  best_geodes_by_blueprint_number = simulate(blueprints, 24)

  print(f"best moves (P1) = {best_geodes_by_blueprint_number}")
  total = 0
  for num, score in best_geodes_by_blueprint_number.items():
    total += num * score

  print(f"quality level (P1) = {total}")

  best_geodes_by_blueprint_number = simulate(blueprints[0:3], 32)

  print(f"best moves (P2) = {best_geodes_by_blueprint_number}")
  total = 1
  for score in best_geodes_by_blueprint_number.values():
    total *= score

  print(f"quality level (P2) = {total}")


if __name__ == '__main__':
    main()
