#To update peak values:
#for each value, check if it is contained in the list of peaks for the problem.
#If so, it is a peak (True), else it is not (False)

import sys

search_file = sys.argv[1]
peak_file = sys.argv[2]

sf = open(search_file, "r")
pf = open(peak_file, "r")

list_of_peaks = list()

for line in pf:
  list_of_peaks.append(int(line.strip()))

for line in sf:
  if "eigen" in line:
    continue

  parts = line.strip().split(",")
  value = int(parts[0])
  if value in list_of_peaks:
    parts[2] = "True"
  else:
    parts[2] = "False"

  new_line = ""
  i = 0
  for part in parts:
    if i == 3:
      new_line += parts[i]
    else:
      new_line += parts[i] + ","
    i += 1

  print(new_line)
