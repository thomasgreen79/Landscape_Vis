#Given graph output from exported Gephi table containing eigenvectory centrality values, sort table numerically by ID
import sys

filename = sys.argv[1]
f = open(filename, "r")

sorted_list = list()

for line in f:
  if "eigen" in line:
    print(line.strip())
  else:
    node_pair = line.strip().split(",")
    node_id = int(node_pair[0])
    node_eig = float(node_pair[1])
    if len(sorted_list) == 0:
      sorted_list.append((node_id,node_eig))
    i = 0
    while i < len(sorted_list) and node_id > sorted_list[i][0]:
      i += 1
    if i == len(sorted_list):
      sorted_list.append((node_id,node_eig))
    else:
      sorted_list.insert(i, (node_id, node_eig))

i = 0
for i in range(0,len(sorted_list)):
  print(str(sorted_list[i][0]) + "," + str(sorted_list[i][1]))
