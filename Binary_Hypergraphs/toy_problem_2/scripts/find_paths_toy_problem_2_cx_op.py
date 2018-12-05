import sys

base = int(sys.argv[1])
num_points = 2**base

def fitness(val):
  if val > 32:
    return 0
  else:
    return val**3 - 60*val**2 + 900*val + 100

def build_string(k_val):
  bin = ''
  for i in range(0, base):
    if i < k_val:
      bin += '0'
    else:
      bin += '1'
  return bin

def cx_op(value, k_val):
  return value ^ int(build_string(k_val), 2)

def get_neighbors(vert_id, num_neighbors):
  neighbors = list()
  neighbors.append(vert_id)
  for i in range(0,num_neighbors):
    neighbors.append(cx_op(vert_id, i))
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
#  print(neighbors)
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

