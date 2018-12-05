import sys, math

base = int(sys.argv[1])
num_points = 2**base

def fitness(val):
  if val > 32:
    return 0
  else:
    return abs(math.exp(val**(1.0/3.0))*math.sin(val))

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

steps = list()
for i in range(0,num_points):
  neighbors = get_neighbors(i, base)
  print(neighbors)
  best_neighbor = get_steepest_ascent(neighbors)
#  if i < best_neighbor:
  edge = str(i) + ";" + str(best_neighbor)
#  else:
#    edge = str(best_neighbor) + ";" + str(i)
  steps.append(edge)

#print(get_neighbors(5, 4))

#print(fitness(504))

for item in steps:
  print(item)
