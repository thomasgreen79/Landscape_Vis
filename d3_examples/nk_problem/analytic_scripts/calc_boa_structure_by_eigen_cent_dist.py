import sys, json

if len(sys.argv) != 2:
  print("Usage: python calc_boa_structure_by_eigen_cent_dist.py <extr_boa_filename.json>")
  sys.exit(1)

boa_filename = sys.argv[1]
boa_read = open(boa_filename, "r")

boa_file_string = boa_read.read()
parsed_json = json.loads(boa_file_string)

eigen_val_counts = dict()

for i in range(0, len(parsed_json["nodes"])):
  node = parsed_json["nodes"][i]
  if node["eigen_cent"] in eigen_val_counts:
    eigen_val_counts[node["eigen_cent"]] += 1
  else:
    eigen_val_counts[node["eigen_cent"]] = 1

for key in eigen_val_counts:
  print(key + ";" + str(eigen_val_counts[key]))
