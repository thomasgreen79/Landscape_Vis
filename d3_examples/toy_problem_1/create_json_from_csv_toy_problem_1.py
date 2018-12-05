import sys, random

base = int(sys.argv[3])
num_points = 2**base

def fitness(val):
  a = 2**(base-1)
  c = 1
  w = 2**(base-7)
  fitness = -1.0
  if val >= (a - w) and val <= (a + w):
    fitness = -c*(1/w**2 + 1/a**2) * (val - a)**2 + 2*c
  else:
    fitness = -(c/a**2) * (val - a)**2 + c
  return fitness


csv_filename = sys.argv[1]
json_filename = sys.argv[2]

fr = open(csv_filename, "r")
fw = open(json_filename, "w")

nodes = list()
edges = dict()
fit_vals = list()

max_fitness = 2.0
#add fitness value for each node
#find and set max fitness value

for line in fr:
  node_pair = line.strip().split(";")
  if node_pair[0] not in nodes:
    nodes.append(node_pair[0])
  if node_pair[1] not in nodes:
    nodes.append(node_pair[1])
  edge = (node_pair[0], node_pair[1])
  if edge not in edges:
    edges[edge] = 1
  else:
    edges[edge] = edges[edge] + 1

fw.write("{\n\"nodes\": [\n")
for i in range(0,len(nodes)):
#  print(str(fitness(int(nodes[i]))))
  fw.write("{\"id\":" + str(nodes[i]) + ", \"group\":1, \"fitness\":" + str(fitness(int(nodes[i]))/max_fitness) + "}")
  if i < len(nodes)-1:
    fw.write(",\n")
  else:
    fw.write("\n")

fw.write("],\n\"links\": [\n")
i = 0
for key in edges:
  fw.write("{\"source\":" + str(key[0]) + ", \"target\":" + str(key[1]) + ", \"value\":" + str(edges[key]) + "}")
  if i < len(edges)-1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1
fw.write("]\n}\n")
