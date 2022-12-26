#!/usr/bin/env python3

from collections import defaultdict

def sample_data():
  return[ (2,2,2),
    (1,2,2),
    (3,2,2),
    (2,1,2),
    (2,3,2),
    (2,2,1),
    (2,2,3),
    (2,2,4),
    (2,2,6),
    (1,2,5),
    (3,2,5),
    (2,1,5),
    (2,3,5),]


def main():
  cubordinates = []
  with open("input.txt", "r") as infile:
    for line in infile:
      cubordinates.append(tuple(int(d) for d in line.split(",")))

  faces: dict[tuple[int, int, int, str], int] = defaultdict(lambda: 0)
  for cube in cubordinates:
    x, y, z = cube
    for face in (
      (x, y, z, "xy"),
      (x, y, z + 1, "xy"),

      (x, y, z, "xz"),
      (x, y + 1, z, "xz"),

      (x, y, z, "yz"),
      (x + 1, y, z, "yz"),
    ):
      faces[face] += 1

  count_distinct = 0
  for value in faces.values():
    if value == 1:
      count_distinct += 1

  print(f"distinct faces = {count_distinct}")

  min_x = min_y = min_z = 1000
  max_x = max_y = max_z = -1000
  for x, y, z in cubordinates:
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

  cubes_set = set(cubordinates)
  visited_air = set()
  faces_seen = 0
  for x in range(min_x - 1, max_x + 2):
    for y in range(min_y - 1, max_y + 2):
      for z in range(min_z - 1, max_z + 2):
        if x != min_x -1 and x != max_x + 2 and y != min_y - 1 and y != max_y + 2 and z != min_z - 1 and z != max_z + 2:
          # Not on edge.
          continue
        # Explore from this tile.
        frontier = [(x, y, z)]
        while frontier:
          curr = frontier.pop()
          if curr in visited_air:
            continue
          visited_air.add(curr)
          # Check six directions for face.
          for offset in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1), (0, 0, 1)):
            next_cube = (curr[0] + offset[0], curr[1] + offset[1], curr[2] + offset[2])
            if next_cube in cubes_set:
              faces_seen += 1
            elif (
              next_cube[0] >= min_x - 1 and next_cube[0] < max_x + 2 and
              next_cube[1] >= min_y - 1 and next_cube[1] < max_y + 2 and
              next_cube[2] >= min_z - 1 and next_cube[2] < max_z + 2
            ):
              # In bounds.
              frontier.append(next_cube)

  print(f"found {faces_seen} new faces")



if __name__ == '__main__':
    main()
