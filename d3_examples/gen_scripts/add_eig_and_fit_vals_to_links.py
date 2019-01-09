import sys, json

#Setup
#*************************************************************************
input_nodes_json_filename = sys.argv[1]
input_network_filename = sys.argv[2]
output_landscape_filename = sys.argv[3]

in_nj_read = open(input_nodes_json_filename, "r")
in_net_read = open(input_network_filename, "r")
out_ls_write = open(output_landscape_filename, "w")

node_string = in_nj_read.read().replace('\n', '\n')
nodes = dict()
edges = dict()


#*************************************************************************
#Variables
max_fitness = 0.0


#*************************************************************************
#Methods

#*************************************************************************
def calc_edge_fit_val(source, target):
  return max(float(nodes[source][0]), float(nodes[target][0]))/max_fitness

def calc_edge_eigen_val(source, target):
  return min(max(float(nodes[source][1]), float(nodes[target][1]))*10, 10)


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

for line in in_net_read:
  node_pair = line.strip().split(';')
  edge = (node_pair[0], node_pair[1])
  if edge in edges:
    continue
  else:
    edges[edge] = (calc_edge_fit_val(edge[0], edge[1]), calc_edge_eigen_val(edge[0], edge[1]))


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
  out_ls_write.write("{\"source\":\"" + key[0] + "\", \"target\":\"" + key[1] + "\", \"fit_val\":\"" + str(edges[key][0]) + "\", \"eigen_val\":\"" + str(edges[key][1]) + "\"}")
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
