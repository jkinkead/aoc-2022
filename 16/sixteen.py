#!/usr/bin/env python3

from dataclasses import dataclass, field
import re
from typing import Optional


@dataclass
class Valve:
  name: str
  rate: int
  links: list["Valve"] = field(default_factory=list)


@dataclass
class State:
  current_valve: Valve
  elephant_valve: Optional[Valve] = None
  # Pressure released through the 30 minutes.
  total_pressure_released: int = 0
  minute: int = 0
  open_valves: set[str] = field(default_factory=set)

  def max_score(self, best_valves: list[Valve]) -> int:
    """
    Returns an upper bound on the best possible score this state can achieve,
    with the given best valves (in order).
    """
    best_score = self.total_pressure_released
    minutes_remaining = 30 - self.minute
    # Assume it takes two minutes to open every valve (one to move, one to
    # open). This will be slightly wrong if we haven't opened the current valve.
    index = 0
    while minutes_remaining > 0 and index < len(best_valves):
      valve_to_check = best_valves[index]
      index += 1
      if valve_to_check.name not in self.open_valves:
        # A valve we can open!
        minutes_remaining -= 1
        if minutes_remaining > 0:
          best_score += minutes_remaining * valve_to_check.rate
        # Move to next room.
        minutes_remaining -= 1

    return best_score

  def clone(self):
    return State(
      current_valve=self.current_valve,
      total_pressure_released=self.total_pressure_released,
      minute=self.minute,
      open_valves=set(self.open_valves),
      elephant_valve=self.elephant_valve,
    )


def main():
  valve_pattern = re.compile(r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([^\n]*)$")
  valves_by_name: dict[str, Valve] = {}
  links_by_name: dict[str, list[str]] = {}
  with open("input.txt", "r") as infile:
    for line in infile:
      match = valve_pattern.search(line)
      assert match is not None, f"bad line {line}"
      name = match.group(1)
      rate = int(match.group(2))
      valves_by_name[name] = Valve(name=name, rate=rate)
      links = match.group(3).split(", ")
      links_by_name[name] = list(links)

  for name, links in links_by_name.items():
    valve = valves_by_name[name]
    for target in links:
      valve.links.append(valves_by_name[target])

  starting_valve = valves_by_name["AA"]
  best_valves = sorted(
    (valve for valve in valves_by_name.values() if valve.rate != 0),
    reverse=True,
    key=lambda v: v.rate
  )

  # Explore valves by best-rate-first.
  for valve in valves_by_name.values():
    valve.links = sorted(valve.links, reverse=True, key=lambda v: v.rate)

  best_score = 0
  frontier = [State(current_valve=starting_valve)]

  # Visited map. Maps room + valves open to max score. Don't explore a room if
  # you've been here on a better path before.
  visited: dict[str, int] = {}
  
  # Do a DFS.
  count = 0
  while len(frontier) > 0:
    count += 1
    curr_state = frontier.pop()

    if curr_state.minute > 30:
      assert False, "should not happen"
    elif curr_state.minute == 30:
      if curr_state.total_pressure_released > best_score:
        best_score = curr_state.total_pressure_released
      continue

    max_score = curr_state.max_score(best_valves)

    if max_score < best_score:
      # Skip. This is not worth exploring.
      continue

    curr_valve = curr_state.current_valve

    key = f"curr={curr_valve.name};visited={sorted(curr_state.open_valves)}"
    if key in visited and visited[key] >= max_score:
      # Skip. This is not worth exploring.
      continue

    visited[key] = max_score

    if curr_valve.rate != 0 and curr_state.current_valve.name not in curr_state.open_valves:
      # Turn on valve in room.
      next_state = curr_state.clone()
      next_state.minute += 1
      next_state.total_pressure_released += (30 - next_state.minute) * curr_valve.rate
      next_state.open_valves.add(curr_valve.name)
      frontier.append(next_state)

    for valve in curr_valve.links:
      # Go to the room, but only actually explore if the 
      next_state = curr_state.clone()
      next_state.minute += 1
      next_state.current_valve = valve
      frontier.append(next_state)

  p1_score = best_score

  # ELEPHANT.
  frontier = [State(current_valve=starting_valve, elephant_valve=starting_valve, minute=4)]
  best_score = 0
  visited = {}

  # Do a DFS.
  count = 0
  while len(frontier) > 0:
    count += 1
    curr_state = frontier.pop()

    if curr_state.minute > 30:
      assert False, "should not happen"
    elif curr_state.minute == 30:
      if curr_state.total_pressure_released > best_score:
        best_score = curr_state.total_pressure_released
      continue

    max_score = curr_state.max_score(best_valves)

    if max_score < best_score:
      # Skip. This is not worth exploring.
      continue

    curr_valve = curr_state.current_valve

    key = f"curr={curr_valve.name};elephant={curr_state.elephant_valve.name};curr_visited={sorted(curr_state.open_valves)}"
    if key in visited and visited[key] >= max_score:
      # Skip. This is not worth exploring.
      continue

    visited[key] = max_score

    # Search self.
    my_next_states = []
    if curr_valve.rate != 0 and curr_valve.name not in curr_state.open_valves:
      # Turn on valve in room.
      next_state = curr_state.clone()
      next_state.minute += 1
      next_state.total_pressure_released += (30 - next_state.minute) * curr_valve.rate
      next_state.open_valves.add(curr_valve.name)
      my_next_states.append(next_state)

    for valve in curr_valve.links:
      # Go to the room.
      next_state = curr_state.clone()
      next_state.minute += 1
      next_state.current_valve = valve
      my_next_states.append(next_state)

    # Search elephant.
    for my_next_state in my_next_states:
      curr_valve = my_next_state.elephant_valve
      if curr_valve.rate != 0 and curr_valve.name not in my_next_state.open_valves:
        # Turn on valve in room.
        next_state = my_next_state.clone()
        next_state.total_pressure_released += (30 - my_next_state.minute) * curr_valve.rate
        next_state.open_valves.add(curr_valve.name)
        frontier.append(next_state)

      for valve in curr_valve.links:
        # Go to the room.
        next_state = my_next_state.clone()
        next_state.elephant_valve = valve
        frontier.append(next_state)
    

  print(f"P1 = {p1_score}. P2 = {best_score}.")


if __name__ == '__main__':
    main()
