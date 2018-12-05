import sys, json

orig_filename = sys.argv[1]
new_filename = sys.argv[2]

fr = open(orig_filename, "r")
fw = open(new_filename, "w")

nodes = dict()
edges = dict()
max_fitness = 0.0

def calc_edge_fit_val(source, target):
  return max(float(nodes[source][0]), float(nodes[target][0]))/max_fitness

def calc_edge_eigen_val(source, target):
  return min(max(float(nodes[source][1]), float(nodes[target][1]))*10, 10)


'''Read JSON and setup nodes dictionary with all values'''
file_string = fr.read()
parsed_json = json.loads(file_string)
for i in range(0,len(parsed_json["nodes"])):
  node = parsed_json["nodes"][i]
  nodes[node["id"]] = (node["fitness"], node["eigen_cent"])
  if float(node["fitness"]) > max_fitness:
    max_fitness = float(node["fitness"])

for i in range(0,len(parsed_json["links"])):
  edge = parsed_json["links"][i]
  source = edge["source"]
  target = edge["target"]
  edges[(source, target)] = (calc_edge_fit_val(source, target), calc_edge_eigen_val(source, target))


'''Use values to write new JSON file with added eigen_val and fit_val for each edge'''
fw.write("{\n\"nodes\": [\n")
i = 0
for key in nodes:
  fw.write("{\"id\":\"" + key + "\", \"group\":1, \"fitness\":\"" + str(nodes[key][0]) + "\", \"eigen_cent\":\"" + str(nodes[key][1]) + "\"}")
  if i < len(nodes)-1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1

fw.write("],\n\"links\": [\n")
i = 0
for key in edges:
  fw.write("{\"source\":\"" + key[0] + "\", \"target\":\"" + key[1] + "\", \"fit_val\":\"" + str(edges[key][0]) + "\", \"eigen_val\":\"" + str(edges[key][1]) + "\"}")
  if i < len(edges)-1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1
fw.write("]\n}\n")
