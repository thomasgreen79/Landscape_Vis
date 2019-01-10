#Given a SAN csv file, find any node that is connected to itself. These will be the peaks of the lanscape
import sys

if len(sys.argv) < 2:
  print("Usage: python find_paths.py <network_filename>")
  sys.exit(0)

network_filename = sys.argv[1]
nf = open(network_filename, "r")

for line in nf:
  nodes = line.split(";")
  if int(nodes[0]) == int(nodes[1]):
    print(str(nodes[0]))
