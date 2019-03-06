import sys

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

in_file = open(input_file_name, "r")
out_file = open(output_file_name, "w")

values = list()
sorted_values = list()

for line in in_file:
  if "eigen" in line:
    continue
  else:
    line_vals = line.strip().split(",")
    values.append((int(line_vals[0]), float(line_vals[1]), int(line_vals[2])))

while len(values) > 0:
  biggest = values[0][1]
  biggest_index = 0
  for i in range(0, len(values)):
    if values[i][1] > biggest:
      biggest = values[i][1]
      biggest_index = i
  sorted_values.append((str(values[biggest_index][0]), str(values[biggest_index][1]), str(values[biggest_index][2])))
  del(values[biggest_index])

for val in sorted_values:
  out_file.write(val[0] + "," + val[1] + "," + val[2] + "\n")
