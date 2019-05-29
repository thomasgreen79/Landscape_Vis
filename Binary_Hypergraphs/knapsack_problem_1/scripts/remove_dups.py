#Removes duplicate edges from EA search results to produce graph that looks better in Gephi visualization
import sys

filename = sys.argv[1]
f = open(filename, 'r')

edges = list()

for line in f:
  trimmed = line.strip()
  if trimmed in edges:
    continue
  else:
    edges.append(trimmed)
    print(trimmed)
