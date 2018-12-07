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
peaks_filename = sys.argv[2]
output_filename = sys.argv[3]

fr_landscape = open(json_filename, "r")
fr_peaks = open(peaks_filename, "r")
fw = open(output_filename, "w")

nodes_peaks = list()


'''Read nodes of landscape and eigen_cent values from files'''
json_landscape_string = fr_landscape.read()
parsed_json = json.loads(json_landscape_string)

for line in fr_peaks:
  nodes_peaks.append(line.strip())

'''Write Nodes as JSON with all values in output file'''
fw.write("{\n\"nodes\": [\n")
i = 0
for i in range(0,len(parsed_json["nodes"])):
  node = parsed_json["nodes"][i]
  is_peak = False
  if node["id"] in nodes_peaks:
    print(str(node["id"]))
    is_peak = True
  fw.write("{\"id\":\"" + str(node["id"]) + "\", \"fitness\":\"" + str(node["fitness"]) + "\", \"eigen_cent\":\"" + node["eigen_cent"] + "\", \"is_peak\": \"" + str(is_peak) + "\"}")
  if i < len(parsed_json["nodes"])-1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1

'''Write Links as JSON as they are without calculated values in output file'''
fw.write("],\n\"links\": [\n")
i = 0

for i in range(0,len(parsed_json["links"])):
  link = parsed_json["links"][i]
  fw.write("{\"source\":\"" + link["source"] + "\", \"target\":\"" + link["target"] + "\", \"fit_val\":\"" + link["fit_val"] + "\", \"eigen_val\":\"" + link["eigen_val"] +"\"}")
  if i < len(parsed_json["links"]) - 1:
    fw.write(",\n")
  else:
    fw.write("\n")
  i += 1

fw.write("]\n}\n")
