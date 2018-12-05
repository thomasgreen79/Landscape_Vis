#Given a table with id's and eigenvector centralities and a file containing all of the peaks of the corresponding SAN landscape, add column to file whose value is true if an ID is a peak and false if not
import sys

eigen_filename = sys.argv[1]
peak_filename = sys.argv[2]

ef = open(eigen_filename, "r")
pf = open(peak_filename, "r")

#collect id's of all peaks in a single list
peak_list = list()
for line in pf:
  peak_list.append(int(line.strip()))

#check all nodes in eigen value file if they are contained in peak list
print("id,eigencentrality,is_peak")
for line in ef:
  if "id" in line:
    continue
  node_pair = line.strip().split(",")
  node_id = int(node_pair[0])
  node_eigen = float(node_pair[1])
  if node_id in peak_list:
    print(str(node_id) + "," + str(node_eigen) + "," + "True")
  else:
    print(str(node_id) + "," + str(node_eigen) + "," + "False")
