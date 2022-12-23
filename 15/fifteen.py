#!/usr/bin/env python3

from dataclasses import dataclass
import re


@dataclass
class Sensor:
  x: int
  y: int
  beacon_dist: int


def p1():
  sensor_pattern = re.compile(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")
  
  target_y = 2000000
  # Projected ranges on target, as inclusive range pairs.
  ranges: list[tuple[int, int]] = []
  beacons_on_target: set[int] = set()
  with open("input.txt", "r") as infile:
    for line in infile:
      match = sensor_pattern.search(line)
      assert match is not None, f"bad line {line}"
      sensor_x = int(match.group(1))
      sensor_y = int(match.group(2))
      beacon_x = int(match.group(3))
      beacon_y= int(match.group(4))
      distance_to_beacon = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y) 
      if beacon_y == target_y:
        beacons_on_target.add(beacon_x)
      assert sensor_y != target_y

      distance_to_target = abs(target_y - sensor_y)
      projection = distance_to_beacon - distance_to_target
      if projection > 0:
        ranges.append([sensor_x - projection, sensor_x + projection])

  ranges = sorted(ranges)
  pruned_ranges = []
  curr_range = ranges[0]
  for r in ranges[1:]:
    if curr_range[1] >= r[0]:
      # Overlap; merge if needed.
      if curr_range[1] < r[1]:
        curr_range[1] = r[1]
    else:
      # No overlap; start new range.
      pruned_ranges.append(curr_range)
      curr_range = r

  pruned_ranges.append(curr_range)

  total_len = -len(beacons_on_target)
  for r in pruned_ranges:
    total_len += r[1] - r[0] + 1

  print(f"P1 = {total_len}")


def p2():
  sensor_pattern = re.compile(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")

  sensors = []
  with open("input.txt", "r") as infile:
    for line in infile:
      match = sensor_pattern.search(line)
      assert match is not None, f"bad line {line}"
      sensor_x = int(match.group(1))
      sensor_y = int(match.group(2))
      beacon_x = int(match.group(3))
      beacon_y= int(match.group(4))
      distance_to_beacon = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y) 
      sensors.append(Sensor(x=sensor_x, y=sensor_y, beacon_dist=distance_to_beacon))

  max_candidate = 4000000

  candidates = []

  for y in range(0, max_candidate + 1):
    ranges = []
    # Check row.
    for sensor in sensors:
      distance_to_target = abs(y - sensor.y)
      projection = sensor.beacon_dist - distance_to_target
      if projection > 0:
        projected_x_min = max(sensor.x - projection, 0)
        projected_x_max = min(sensor.x + projection, max_candidate)
        ranges.append([projected_x_min, projected_x_max])
    ranges = sorted(ranges)
    pruned_ranges = []
    curr_range = ranges[0]
    for r in ranges[1:]:
      if curr_range[1] >= r[0]:
        # Overlap; merge if needed.
        if curr_range[1] < r[1]:
          curr_range[1] = r[1]
      else:
        # No overlap; start new range.
        pruned_ranges.append(curr_range)
        curr_range = r

    pruned_ranges.append(curr_range)
    if len(pruned_ranges) != 1:
      assert len(pruned_ranges) == 2, f"more than one answer: {pruned_ranges}"
      assert pruned_ranges[0][0] == 0, f"more than one answer: {pruned_ranges}"
      assert pruned_ranges[1][1] == max_candidate, f"more than one answer: {pruned_ranges}"
      candidate_x = pruned_ranges[0][1] + 1
      candidates.append((candidate_x, y))
    elif pruned_ranges[0][0] != 0:
      print(f"found candidate at ({pruned_ranges[0][0]}, {y}).")
      assert pruned_ranges[0][0] == 1, f"bad range at {y}: {pruned_ranges}"
      candidates.append((0, y))
    elif pruned_ranges[0][1] != max_candidate:
      assert pruned_ranges[0][1] == max_candidate - 1, f"bad range at {y}: {pruned_ranges}"
      candidates.append((max_candidate, y))

  assert len(candidates) == 1, f"found more than one answer: {candidates}"

  print(f"P2 = {candidates[0][0] * 4000000 + candidates[0][1]}")


def main():
  p1()
  p2()


if __name__ == '__main__':
    main()
