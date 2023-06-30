import sys
from pprint import pprint
from copy import deepcopy
import time
import numpy as np
import heapq


def test(input_grid, output_grid, no_req3=False):
  assert len(input_grid) == len(output_grid)
  assert len(input_grid[0]) == len(output_grid[0])

  # requirement 1
  for i in range(len(output_grid)):
    for j in range(len(output_grid[i])):
      if output_grid[i][j] > input_grid[i][j]:
        raise Exception(f"Grid increased at {i}, {j}: {output_grid[i][j]} > {input_grid[i][j]}")

  # requirement 2
  neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))
  for i in range(len(output_grid)):
    for j in range(len(output_grid[i])):
      val = output_grid[i][j]
      for di, dj in neighbors:
        ni = i + di
        nj = j + dj
        if ni < 0 or ni >= len(output_grid) or nj < 0 or nj >= len(output_grid[0]):
          continue
        if output_grid[ni][nj] > 2 * val:
          raise Exception(f"Neighbor constraint violated {i},{j} {ni},{nj}: {output_grid[ni][nj]} > 2 * {val}")


  # requirement 3
  if not no_req3:
    for i in range(len(output_grid)):
      for j in range(len(output_grid[i])):
        new_grid = deepcopy(output_grid)
        new_grid[i][j] += 1
        try:
          test(input_grid, output_grid, no_req3=True)
          raise Exception(f"Grid could be bigger at {i},{j}")
        except Exception:
          pass

def out_of_bounds(g, i, j):
  return i < 0 or i >= len(g) or j < 0 or j >= len(g[0])

def func1(g):
  g = deepcopy(g)
  neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))
  def visit(g, i, j, visited):
    if out_of_bounds(g, i, j):
      return
    if (i, j) in visited:
      return

    neighbor_vals = [g[i][j]] + [
        2 * g[i + di][j + dj] for di, dj in neighbors if not out_of_bounds(g, i + di, j + dj)]
    v = min(neighbor_vals)
    g[i][j] = v
    visited.add((i, j))

    for di, dj in neighbors:
      visit(g, i + di, j + dj, visited)

  for i in range(len(g)):
    for j in range(len(g[0])):
      visit(g, i, j, set())

  return g


def func2(g):
  g = deepcopy(g)
  completed = [[False] * len(g[0]) for _ in range(len(g))]

  def calculateValue(x, y, pastVal):
    if x < 0 or x > len(g)-1 or y < 0 or y > len(g[0])-1:
      return 

    pv = pastVal * 2
    cv = g[x][y]
    if cv < pv:
      pv = cv
    if pv < g[x][y]:
      completed[x][y] = False
    if completed[x][y]:
      return

    g[x][y] = pv
    completed[x][y] = True
    val = pv
    calculateValue(x,   y+1, val)
    calculateValue(x,   y-1, val)
    calculateValue(x+1, y, val)
    calculateValue(x-1, y, val)

  minval = min((v for row in g for v in row))
  for i in range(len(g)):
    for j in range(len(g[0])):
      val = g[i][j]
      if val == minval:
        g[i][j] = val
        completed[i][j] = True
        calculateValue(i, j+1, val)
        calculateValue(i, j-1, val)
        calculateValue(i+1, j, val)
        calculateValue(i-1, j, val) 

  return g


def func3(g):
  g = deepcopy(g)
  completed = [[False] * len(g[0]) for _ in range(len(g))]

  def calculateValue(x, y, pastVal):
    if x < 0 or x > len(g)-1 or y < 0 or y > len(g[0])-1:
      return 

    nv = 2 * pastVal
    gv = g[x][y]
    if nv < gv:
      pv = nv
    elif completed[x][y]:
      return
    else:
      pv = gv

    g[x][y] = pv
    completed[x][y] = True
    calculateValue(x,   y+1, pv)
    calculateValue(x,   y-1, pv)
    calculateValue(x+1, y, pv)
    calculateValue(x-1, y, pv)

  calculateValue(0, 0, g[0][0])

  return g


def func4(g):
  g = deepcopy(g)
  width, height = len(g[0]), len(g)

  heap = [(g[x][y], x, y) for x in range(height) for y in range(width)]
  heapq.heapify(heap)

  visited = [[False] * width for _ in range(height)]
  total_items = len(heap)
  visited_count = 0

  heappop = heapq.heappop
  heappush = heapq.heappush

  while visited_count < total_items:
    value, x, y = heappop(heap)
    if visited[x][y]:
      continue

    visited[x][y] = True
    visited_count += 1
    g[x][y] = value

    # Smooth out the neighbors.
    max_neighbor_value = 2 * value
    if x > 0 and not visited[x - 1][y]:
      heappush(heap, (max_neighbor_value, x - 1, y))
    if x < height - 1 and not visited[x + 1][y]:
      heappush(heap, (max_neighbor_value, x + 1, y))
    if y > 0 and not visited[x][y - 1]:
      heappush(heap, (max_neighbor_value, x, y - 1))
    if y < width - 1 and not visited[x][y + 1]:
      heappush(heap, (max_neighbor_value, x, y + 1))

  return g

def run_test_cases(func, cases):
  before = time.time()
  outputs = [func(case) for case in cases]
  after = time.time()
  print(f"Ran {func} in {after - before}s")

  for input_grid, output_grid in zip(cases, outputs):
    try:
      test(input_grid, output_grid, True)
      if False:
        print("PASS")
        print(np.array(input_grid))
        print(" ->")
        print(np.array(output_grid))
        print("*"*20)
    except Exception as e:
      print("FAIL")
      print(np.array(input_grid))
      print(" ->")
      print(np.array(output_grid))
      raise


def test_func(func):
  cases = (
    [
      [1],
    ],
    [
      [1, 4],
    ],
    [
      [1, 4, 8],
    ],
    [
      [1, 8],
      [2, 4],
    ],
    [
      [1, 2],
      [8, 4],
    ],
  )

  run_test_cases(func, cases) 

  np.random.seed(1337)
  num_random = 1000
  random_cases = np.random.randint(1, 100, (num_random, 30, 30)).tolist()
  run_test_cases(func, random_cases) 

  n = 20
  pathological = [[0] * n for _ in range(n)]
  v = 1.0
  for i in range(n):
    for j in range(n):
      pathological[i][j] = v
      v = v * 1.1
  run_test_cases(func, [pathological] * 100) 

def main():
  sys.setrecursionlimit(5000)

  test_func(func1)
  # test_func(func2)
  #test_func(func3)
  #test_func(func4)


if __name__ == "__main__":
  main()
