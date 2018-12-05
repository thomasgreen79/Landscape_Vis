#Creates a fabricated graph of size n which follows linearly from the first nodeall the way to the nth node in a single path

#Check to see shape of fitness vs. eigenvector centrality plot.

import sys

base = int(sys.argv[1])
num_nodes = 2**base

for i in range(0,num_nodes-1):
  print(str(i) + ";" + str(i+1))
print(str(num_nodes-1) + ";" + str(num_nodes-1))

