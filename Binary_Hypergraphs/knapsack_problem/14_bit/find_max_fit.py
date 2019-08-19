import sys

filename = sys.argv[1]

fit_read = open(filename, "r")

max_fit = 0
max_val = "0"

for line in fit_read:
  if "id" in line:
    continue
  else:
    components = line.strip().split(",")
    fit = float(components[1])
    if fit > max_fit:
      max_fit = fit
      max_val = components[0]

print("Max fitness is: " + str(max_fit) + " at value: " + max_val)
