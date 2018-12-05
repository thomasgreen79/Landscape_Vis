#Given a SAN csv file, find any node that is connected to itself. These will be the peaks of the lanscape
import sys

filename = sys.argv[1]
f = open(filename, "r")

for line in f:
  nodes = line.split(";")
  if int(nodes[0]) == int(nodes[1]):
    print(str(nodes[0]))
