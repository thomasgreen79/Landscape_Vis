#Removes excess output from EA search to produce graph file readable by Gephi
import sys

filename = sys.argv[1]
output_filename = sys.argv[2]

f = open(filename, 'r')
fw = open(output_filename, 'w')

line_count = 0
skip_count = 0

for line in f:
  if line_count == 40 and skip_count < 3:
    skip_count += 1
    if skip_count == 3:
      line_count = 0
      skip_count = 0
    continue
  else:
    fw.write(line)
    line_count += 1
