'''
Given json file of landscape with fitness values and csv file with corresponding eigen_cent values
  Read json landscape into parsed_json
  Read eigen_cent values into dictionary
  For every id in json-nodes
    print out json of node - id, group, fitness, eig_cent
  For every link in json-links
    print out as is (to be processed by add fit, eig_cent scores script)
'''
import sys, json

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

json_filename = sys.argv[1]
eig_cent_filename = sys.argv[2]
output_filename = sys.argv[3]
hyper_cube_filename = sys.argv[4]

fr_landscape = open(json_filename, "r")
fr_eig_cent = open(eig_cent_filename, "r")
fw = open(output_filename, "w")
fr_hyper = open(hyper_cube_filename, "r")

num_edges = file_len(hyper_cube_filename)
nodes_eig_cent = dict()


'''Read nodes of landscape and eigen_cent values from files'''
json_landscape_string = fr_landscape.read()
parsed_json = json.loads(json_landscape_string)

for line in fr_eig_cent:
  if "eigencentrality" in line:
    continue
  vals = line.split(',')
  nodes_eig_cent[vals[0]] = (vals[1].strip(), vals[2].strip())

'''Write Nodes as JSON with all values in output file'''
fw.write("{\n\"nodes\": [\n")
i = 0
for key in nodes_eig_cent:
  node = nodes_eig_cent[key]
  fw.write("{\"id\":\"" + str(key) + "\", \"group\":1, \"fitness\":\"" + str(parsed_json["nodes"][int(key)]["fitness"]) + "\", \"eigen_cent\":\"" + str(node[0]) + "\"}")
  if i < len(nodes_eig_cent)-1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1

'''Write Links as JSON as they are without calculated values in output file'''
fw.write("],\n\"links\": [\n")
i = 0
####Need to create a file with all of the edges of the hypercube for this problem###
for line in fr_hyper:
  pair = line.strip().split(";")
  fw.write("{\"source\":\"" + pair[0] + "\", \"target\":\"" + pair[1] + "\"}")
  if i < num_edges - 1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1

fw.write("]\n}\n")

