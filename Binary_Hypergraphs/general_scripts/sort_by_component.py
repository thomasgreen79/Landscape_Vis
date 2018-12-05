#Given graph output from exported Gephi table containing eigenvectory centrality values, sort table numerically by component number
import sys

filename = sys.argv[1]
f = open(filename, "r")

sorted_list = list()

for line in f:
  if "component" in line:
    continue
  node_pair = line.strip().split("\t")
  node_id = int(node_pair[0])
  node_comp = int(node_pair[1])
  if len(sorted_list) == 0:
    sorted_list.append((node_id,node_comp))
  else:
    i = 0
    while i < len(sorted_list) and node_comp > sorted_list[i][1]:
      i += 1
    j = 0
    while i+j < len(sorted_list) and node_id > sorted_list[i+j][0] and node_comp == sorted_list[i+j][1]:
      j += 1

    if i+j == len(sorted_list):
      sorted_list.append((node_id,node_comp))
    else:
      sorted_list.insert(i+j, (node_id, node_comp))

i = 0
for i in range(0,len(sorted_list)):
  print(str(sorted_list[i][0]) + "," + str(sorted_list[i][1]))
