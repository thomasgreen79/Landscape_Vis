'''Check if a landscape SAN json file has any loops (peaks listed with both nodes same value)'''
import sys

filename = sys.argv[1]

f = open(filename, "r")

for line in f:
  if "source" in line:
    split_line = line.split(' ')
    src_tar = (split_line[0].split('"')[3], split_line[1].split('"')[3])
    
    if int(src_tar[0]) == int(src_tar[1]):
      print(src_tar[0] + "\t" + src_tar[1])
