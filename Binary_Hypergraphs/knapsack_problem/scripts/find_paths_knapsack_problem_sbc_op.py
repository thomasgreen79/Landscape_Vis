import sys

base = int(sys.argv[1])
num_points = 2**base
W = int(sys.argv[2])

#Could initialize randomly
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


def flip_bit(value, bit_index):
  value ^= (1 << bit_index)
  return value

def get_neighbors(vert_id, num_neighbors):
  neighbors = list()
  neighbors.append(vert_id)
  for i in range(0,num_neighbors):
    neighbors.append(flip_bit(vert_id, i))
  return neighbors

def get_steepest_ascent(neighbors):
  max_ascent_index = -1
  max_ascent_value = -1
  for i in range(0, len(neighbors)):
    score = fitness(neighbors[i])
    if score > max_ascent_value:
      max_ascent_value = score
      max_ascent_index = i
  return neighbors[max_ascent_index]

max_num = -1
max_fit = 0
steps = list()
for i in range(0,num_points):
  fit = fitness(i)
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, base)
  best_neighbor = get_steepest_ascent(neighbors)
  edge = str(i) + ";" + str(best_neighbor)
  steps.append(edge)


for item in steps:
  print(item)

print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
