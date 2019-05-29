import sys

filename = sys.argv[1]
base = sys.argv[2]
W = int(sys.argv[3])
f = open(filename, "r")

wt = [2, 5, 7, 3, 1, 4, 10, 14, 6, 8, 12, 15, 13, 9]
val = [20, 30, 35, 12, 3, 15, 50, 60, 25, 32, 62, 75, 68, 42]


def fitness(value):
  format_string = '{0:0' + str(base) + 'b}'
#  fitness = -1.0
  curr_wt = 0
  curr_val = 0
  bit_string = format_string.format(value)
  index = 0
  for c in bit_string:
    if int(c) == 1:
      curr_wt += wt[index]
      curr_val += val[index]
      if curr_wt > W:
        return 0
    index += 1
  return curr_val


for line in f:
  if "eigen" in line:
    print(line.strip() + ",fitness")
  else:
    print(line.strip() + "," + str(fitness(int(line.split(",")[0]))))
