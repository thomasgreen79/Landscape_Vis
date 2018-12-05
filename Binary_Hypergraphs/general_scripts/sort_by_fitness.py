#Given graph output from exported Gephi table containing eigenvectory centrality values, sort table numerically by ID
import sys

filename = sys.argv[1]
f = open(filename, "r")

sorted_list = list()

for line in f:
  if "eigen" in line:
    print(line.strip())
  else:
    node_trip = line.strip().split(",")
    node_id = int(node_trip[0])
    node_eig = float(node_trip[1])
    node_fit = float(node_trip[2])
    if len(sorted_list) == 0:
      sorted_list.append((node_id,node_eig,node_fit))
      continue
    i = 0

    while i < len(sorted_list) and node_fit < sorted_list[i][2]:
      i += 1
    if i == len(sorted_list):
      sorted_list.append((node_id,node_eig,node_fit))
    elif node_fit == sorted_list[i][2]:
      j = 0
      while (i+j) < len(sorted_list) and node_id > sorted_list[i+j][0] and node_fit == sorted_list[i+j][2]:
        j += 1
      if i+j == len(sorted_list):
        sorted_list.append((node_id,node_eig,node_fit))
      else:
        sorted_list.insert(i+j, (node_id,node_eig,node_fit))
    else:
      sorted_list.insert(i, (node_id,node_eig,node_fit))

i = 0
for i in range(0,len(sorted_list)):
  print(str(sorted_list[i][0]) + "," + str(sorted_list[i][1]) + "," + str(sorted_list[i][2]))
