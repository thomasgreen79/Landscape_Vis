import sys

data_filename = sys.argv[1]
fitness_filename = sys.argv[2]
df = open(data_filename, "r")
ff = open(fitness_filename, "r")

fitnesses = dict()

#Setup dictionary with all fitnesses
for line in ff:
  if "id" in line:
    continue
  pair = line.strip().split(",")
  fitnesses[pair[0]] = pair[1]

#Add fitnesses to data file
for line in df:
  if "eigen" in line:
    print(line.strip() + ",fitness")
  else:
    print(line.strip() + "," + fitnesses[line.strip().split(",")[0]])
