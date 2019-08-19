'''
Create a list of all nodes and probabilities of neighbors as randomly equal with the exception of peaks which only connect to themselves.
'''

import sys

if len(sys.argv) < 4:
  print("Usage ...")
  sys.exit(1)

problem_size = int(sys.argv[1])
peaks_file_name = sys.argv[2]
output_RAN_file_name = sys.argv[3]

peaks_read = open(peaks_file_name, "r")
output_RAN_write = open(output_RAN_file_name, "w")

peaks = list()

def flip_bit(value, bit_index):
  value ^= (1 << bit_index)
  return value

def get_neighbors(node_id):
  neighbors = list()
  for i in range(0,problem_size):
    neighbors.append(flip_bit(node_id, i))
  return neighbors

for line in peaks_read:
  peaks.append(int(line.strip()))

for i in range(0, 2**problem_size):
  if i in peaks:
    output_RAN_write.write(str(i) + ";" + str(i) + ";" + "1.0\n")
  else:
    neighbors = get_neighbors(i)
    for neighbor in neighbors:
      output_RAN_write.write(str(i) + ";" + str(neighbor) + ";" + str(1.0/problem_size) + "\n")
