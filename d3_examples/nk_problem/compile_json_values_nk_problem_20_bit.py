import sys


net_filename = sys.argv[1]
fit_filename = sys.argv[2]
eigen_filename = sys.argv[3]
peak_filename = sys.argv[4]
json_filename = sys.argv[5]

net_read = open(net_filename, "r")
fit_read = open(fit_filename, "r")
eigen_read = open(eigen_filename, "r")
peak_read = open(peak_filename, "r")
json_write = open(json_filename, "w")

nodes = list()
edges = dict()
fitnesses = dict()
eigen_cents = list()
peaks = list()

max_fitness = 0.0

#add fitness value for each node
#find and set max fitness value

for line in net_read:
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

for line in fit_read:
  if "id" in line:
    continue
  id_fit = line.strip().split(",")
  if id_fit[0] not in fitnesses:
    fitnesses[id_fit[0]] = id_fit[1]

#Read peaks
#Read eigen_values

#Add in hypercube for all edges somehow

#Figure out order to process everything to compile all values as easily as possible for writing to json file

#Look into writing code to see what needs to change...



max_fitness = max(fit_vals)
print(max_fitness)

fw.write("{\n\"nodes\": [\n")
for i in range(0,len(nodes)):
#  print(str(fitness(int(nodes[i]))))
  fw.write("{\"id\":\"" + str(nodes[i]) + "\", \"group\":\"1\", \"fitness\":\"" + str(fitness(np.array(int2bits(int(nodes[i]), N), dtype=bool), contrs, fit_mem)/max_fitness) + "\"}")
  if i < len(nodes)-1:
    fw.write(",\n")
  else:
    fw.write("\n")

fw.write("],\n\"links\": [\n")
i = 0
for key in edges:
  if key[0] != key[1]:
    fw.write("{\"source\":\"" + str(key[0]) + "\", \"target\":\"" + str(key[1]) + "\", \"value\":\"" + str(edges[key]) + "\"}")
    if i < len(edges)-1:
      fw.write(",\n")
    else:
      fw.write("\n")
  i += 1
fw.write("]\n}\n")
