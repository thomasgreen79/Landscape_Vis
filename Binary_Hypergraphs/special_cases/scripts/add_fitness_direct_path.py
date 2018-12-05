import sys

filename = sys.argv[1]
base = int(sys.argv[2])
f = open(filename, "r")


def fitness(value):
  num_nodes = 2**base
  return value/num_nodes

for line in f:
  if "eigen" in line:
    print(line.strip() + ",fitness")
  else:
    print(line.strip() + "," + str(fitness(int(line.split(",")[0]))))
