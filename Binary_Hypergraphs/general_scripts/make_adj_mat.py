import sys

#filename = 'toy_problem_paths_3_bit.csv'
filename = sys.argv[1]
f = open(filename, 'r')

adj_mat = [[0 for x in range(8)] for y in range(8)]

for line in f:
  pair = [x.strip() for x in line.split(';')]
  adj_mat[int(pair[0])][int(pair[1])] = 1

print(str(adj_mat).replace('[', '').replace(']','\n').replace(',', ''))
