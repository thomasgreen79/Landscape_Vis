'''
With input files containing data for the SAN network (redundant since link info is handled separately), fitness values, eigen_centrality values, and peak ids, this script reads all values and creates final json formatted data for all nodes in network.

The link data still needs to be created via either hypercube or SAN network, depending on desired
landscape visualization
'''

import sys

if len(sys.argv) < 7:
  print("Usage: python compile_node_values_json.py <network_filename.csv> <fitness_filename.csv> <eigen_cents_filename.csv> <boa_peaks_filename> <peaks_filename.csv> <output_filename.json>")
  sys.exit(0)

net_filename = sys.argv[1]
fit_filename = sys.argv[2]
eigen_filename = sys.argv[3]
boa_peaks_filename = sys.argv[4]
peak_filename = sys.argv[5]
json_filename = sys.argv[6]

net_read = open(net_filename, "r")
fit_read = open(fit_filename, "r")
eigen_read = open(eigen_filename, "r")
peak_read = open(peak_filename, "r")
boa_peaks_read = open(boa_peaks_filename, "r")
json_write = open(json_filename, "w")

nodes = dict()
edges = dict()
fitnesses = list()
boa_peaks = list()
#eigen_cents = list()
peaks = list()

max_fitness = 0.0
eigen_boost = 0.001

def sort_by_boa_size(nodes_dict):
  temp_nodes = dict(nodes_dict) #Make copy of dictionary to preserve original
  sorted_nodes = list()
  max_boa_size = -1
  while max_boa_size != 0:
    max_key = None
    max_boa_size = -1
    for key in temp_nodes:
      if int(temp_nodes[key][3]) > max_boa_size:
        max_key = key
        max_boa_size = int(temp_nodes[key][3])
    max_node = temp_nodes[max_key]
    sorted_nodes.append((max_key, max_node[0], max_node[1], max_node[2], max_node[3], max_node[4]))
    del temp_nodes[max_key]
  for key in temp_nodes:
    new_node = temp_nodes[key]
    sorted_nodes.append((key, new_node[0], new_node[1], new_node[2], new_node[3], new_node[4]))
  return sorted_nodes

  

#add fitness value for each node
#find and set max fitness value

for line in net_read:
  node_pair = line.strip().split(";")
  if node_pair[0] not in nodes:
    nodes[node_pair[0]] = (node_pair[0])
  if node_pair[1] not in nodes:
    nodes[node_pair[1]] = (node_pair[1])

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
    fitnesses.append(float(id_fit[1]))
  if id_fit[0] not in nodes:
    print("Missing: " + id_fit[0])
  else:
    nodes[id_fit[0]] = (id_fit[1])


for line in eigen_read:
  if "id" in line:
    continue
  id_eigen = line.strip().split(",")
  if id_eigen[0] not in nodes:
    print("Missing: " + id_eigen[0])
  else:
    nodes[id_eigen[0]] = (nodes[id_eigen[0]], str(float(id_eigen[1]) + eigen_boost))


for line in peak_read:
  peak = line.strip()
  if peak not in peaks:
    peaks.append(peak)
  else:
    print("Repeated peak: " + peak)


for line in boa_peaks_read:
  if "id" in line:
    continue
  id_boa_peak = line.strip().split(",")
  if id_boa_peak[0] not in nodes:
    print("Missing: " + id_boa_peak[0])
  elif id_boa_peak[0] in peaks:
    nodes[id_boa_peak[0]] = (nodes[id_boa_peak[0]][0], nodes[id_boa_peak[0]][1], id_boa_peak[1], id_boa_peak[2], "True")
  else:
    nodes[id_boa_peak[0]] = (nodes[id_boa_peak[0]][0], nodes[id_boa_peak[0]][1], id_boa_peak[1], 0, "False")
    
#Look into writing code to see what needs to change...

max_fitness = max(fitnesses)
print(max_fitness)

json_write.write("{\n\"nodes\": [\n")
sorted_by_boa_size = sort_by_boa_size(nodes)
for i in range(0, len(sorted_by_boa_size)):
  print_node = sorted_by_boa_size[i]
#  is_peak_val = "False"
#  if key in peaks:
#    is_peak_val = "True"

  json_write.write("{\"id\":\"" + str(print_node[0]) + "\", \"fitness\":\"" + str(float(print_node[1])/max_fitness) + "\", \"eigen_cent\":\"" + str(print_node[2]) + "\", \"boa_peak\":\"" + str(print_node[3]) + "\", \"boa_size\": \"" + str(print_node[4]) + "\", \"is_peak\": \"" + print_node[5] + "\"}")

  if i < len(sorted_by_boa_size)-1:
    json_write.write(",\n")
  else:
    json_write.write("\n")
  i += 1

json_write.write("]}\n")

