import sys

base = int(sys.argv[1])
num_points = 2**base
W = int(sys.argv[2])

#Could initialize randomly
wt = [2, 5, 7, 3, 1, 4, 10, 14, 6, 8, 12, 15, 13, 9]
val = [20, 30, 35, 12, 3, 15, 50, 60, 25, 32, 62, 75, 68, 42]


def fitness(value):
  format_string = '{0:0' + str(base) + 'b}'
#  fitness = -1.0
  curr_wt = 0
  curr_val = 0
  bit_string = format_string.format(value)
  index = 0
  for c in bit_string:
    if int(c) == 1:
      curr_wt += wt[index]
      curr_val += val[index]
      if curr_wt > W:
        return 0
    index += 1
  return curr_val


csv_filename = sys.argv[3]
json_filename = sys.argv[4]

fr = open(csv_filename, "r")
fw = open(json_filename, "w")

nodes = list()
edges = dict()
fit_vals = list()

#max_fitness = 225.0
max_fitness = 0.0
#add fitness value for each node
#find and set max fitness value

for line in fr:
  node_pair = line.strip().split(";")
  if node_pair[0] not in nodes:
    nodes.append(node_pair[0])
    fit_vals.append(fitness(int(node_pair[0])))
#  if node_pair[1] not in nodes:
#    nodes.append(node_pair[1])
#    fit_vals.append(fitness(int(node_pair[1])))
  edge = (node_pair[0], node_pair[1])
  if edge not in edges:
    edges[edge] = 1
  else:
    edges[edge] = edges[edge] + 1

max_fitness = max(fit_vals)
print(max_fitness)

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
