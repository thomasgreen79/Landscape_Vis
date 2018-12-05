'''Check if a landscape SAN json file has any loops (peaks listed with both nodes same value)'''
import sys

filename = sys.argv[1]

f = open(filename, "r")

for line in f:
  if "source" in line:
    split_line = line.split(' ')
    src_tar = (split_line[0].split(':')[1].split(',')[0], split_line[1].split(':')[1].split(',')[0])
    if src_tar[0] == src_tar[1]:
      continue
    else:
      print(line.strip())
  else:
    print(line.strip())
