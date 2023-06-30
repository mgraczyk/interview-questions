
def answer1(first, second):
  from collections import defaultdict

  # input: first, second - list
  dic = defaultdict(list)
  for first_group, color_group in zip(first, second):
    for i in range(len(first_group)):
      dic[first_group[i]].append(color_group[i])
      if len(dic[first_group[i]]) > len(first):
        return False
      
  dic.sort(key=lambda x: len(dic[x]), reverse=True)

  res = [[0 for j in range(len(first[i]))] for i in range(first)]

  group = len(first)
  idx = 0
  idx2 = 0
  for k, v in dic.items:
    for color in v:
      res[idx][idx2] = str(k) + color
      idx += 1
      if idx == group:
        idx = 0
        idx2 += 1
        

def main():
  inputs = [
      (
        [(8, 2, 9), (4, 6, 4), (4, 5, 1)],
        [('r', 'g', 'b'), ('w', 'c', 'b'), ('x', 'y', 'b')],
      )
  ]

  for first, second in inputs:
    output = answer1(first, second)
    print(output)

if __name__ == "__main__":
  main()
