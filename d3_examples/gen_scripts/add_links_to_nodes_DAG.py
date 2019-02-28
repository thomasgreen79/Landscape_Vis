import sys, json

#Setup
#*************************************************************************
if len(sys.argv) < 4:
  print("Usage: python add_links_to_nodes_DAG.py <nodes_filename.json> <links_filename_SAN.csv> <output_landscape_filename.json>")
  sys.exit(0)

input_nodes_json_filename = sys.argv[1]
input_network_filename = sys.argv[2]
#input_boa_peaks_filename = sys.argv[3]
output_landscape_filename = sys.argv[3]

in_nj_read = open(input_nodes_json_filename, "r")
in_net_read = open(input_network_filename, "r")
#in_boa_read = open(input_boa_peaks_filename, "r")
out_ls_write = open(output_landscape_filename, "w")

node_string = in_nj_read.read()
nodes = dict()
edges = dict()
boa_peaks = dict()
boa_indexes = dict()
boa_index = 0


#*************************************************************************
#Variables
max_fitness = 0.0


#*************************************************************************
#Methods

#*************************************************************************
def calc_edge_fit_val(source, target):
  return max(float(nodes[source][0]), float(nodes[target][0]))/max_fitness

def calc_edge_eigen_val(source, target):
  return min(((float(nodes[source][1]) + float(nodes[target][1]))/2)*20, 10)
  #return min(max(float(nodes[source][1]), float(nodes[target][1]))*10, 10)

def calc_boa_peak_index(peak_1, peak_2):
  if peak_1 == peak_2:
    return boa_indexes[peak_1]
  else:
    return -1

def calc_boa_peak(peak_1, peak_2):
  if peak_1 == peak_2:
    return peak_1
  else:
    return -1

#*************************************************************************
#Script_Code

#*************************************************************************
'''Read data into memory'''
#file_string = in_nj_read.read()
file_string = node_string
parsed_json = json.loads(file_string)

for i in range(0,len(parsed_json["nodes"])):
  node = parsed_json["nodes"][i]
  nodes[node["id"]] = (node["fitness"], node["eigen_cent"])
  if float(node["fitness"]) > max_fitness:
    max_fitness = float(node["fitness"])
  boa_peaks[node["id"]] = node["boa_peak"]
  if node["boa_peak"] not in boa_indexes:
    boa_indexes[node["boa_peak"]] = boa_index
    boa_index += 1


for line in in_net_read:
  node_pair = line.strip().split(';')
  edge = (node_pair[0], node_pair[1])
  if edge in edges or node_pair[0] == node_pair[1]:
    continue
  else:
    edges[edge] = (calc_edge_fit_val(edge[0], edge[1]), calc_edge_eigen_val(edge[0], edge[1]), calc_boa_peak_index(boa_peaks[edge[0]], boa_peaks[edge[1]]), calc_boa_peak(boa_peaks[edge[0]], boa_peaks[edge[1]]))


'''
for i in range(0,len(parsed_json["links"])):
  edge = parsed_json["links"][i]
  source = edge["source"]
  target = edge["target"]
  edges[(source, target)] = (calc_edge_fit_val(source, target), calc_edge_eigen_val(source, target))
'''

'''Write nodes and links to landscape file'''
out_ls_write.write(node_string[0:len(node_string)-2])
#json.dump(parsed_json, out_ls_write)

out_ls_write.write(",\n\"links\": [\n")
i = 0
for key in edges:
  out_ls_write.write("{\"source\":\"" + key[0] + "\", \"target\":\"" + key[1] + "\", \"fit_val\":\"" + str(edges[key][0]) + "\", \"eigen_val\":\"" + str(edges[key][1]) + "\", \"boa_color_index\":\"" + str(edges[key][2]) + "\", \"boa_peak\":\"" + str(edges[key][3]) + "\"}")
  if i < len(edges)-1:
    out_ls_write.write(",\n")
  else:
    out_ls_write.write("\n")
  i += 1
out_ls_write.write("]\n}\n")
'''
fw.write("{\n\"nodes\": [\n")
i = 0
for key in nodes:
  fw.write("{\"id\":\"" + key + "\", \"group\":1, \"fitness\":\"" + str(nodes[key][0]) + "\", \"eigen_cent\":\"" + str(nodes[key][1]) + "\"}")
  if i < len(nodes)-1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1
'''
