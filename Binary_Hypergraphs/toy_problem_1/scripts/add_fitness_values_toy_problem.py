import sys

filename = sys.argv[1]
base = int(sys.argv[2])
f = open(filename, "r")


def fitness(val):
  a = 2**(base-1)
  c = 1
  w = 2**(base-7)
  fitness = -1.0
  if val >= (a - w) and val <= (a + w):
    fitness = -c*(1/w**2 + 1/a**2) * (val - a)**2 + 2*c
  else:
    fitness = -(c/a**2) * (val - a)**2 + c
  return fitness

'''
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
'''

for line in f:
  if "eigen" in line:
    print(line.strip() + ",fitness")
  else:
    print(line.strip() + "," + str(fitness(int(line.split(",")[0]))))
