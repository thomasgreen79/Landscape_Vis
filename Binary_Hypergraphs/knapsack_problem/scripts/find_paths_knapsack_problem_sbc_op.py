import sys
import numpy as np
from numpy import random

np.random.seed(19)

if len(sys.argv) < 8:
  print("Usage: python find_paths_knapsack_problem_sbc_op.py <num_elements> <max_weight> <nth rank> <network_output_filename.csv> <fitness_output_filename.csv> <boa_peaks_filename.csv> <peaks_filename.txt>")
  sys.exit(0)


base = int(sys.argv[1])
num_points = 2**base
W = int(sys.argv[2])
n = int(sys.argv[3])

#Could initialize randomly
wt = [2, 5, 7, 3, 1, 4, 10, 14, 6, 8, 12, 15, 13, 9]
val = [20, 30, 35, 12, 3, 15, 50, 60, 25, 32, 62, 75, 68, 42]


#Adding two lists for UF code for Basin of Attraction data
boa_uf = list()
size_uf = list()

#Initialize Union Find "arrays"
for i in range(0,num_points):
  boa_uf.append(i)
  size_uf.append(1)

SAN_file_name = sys.argv[4]
fit_file_name = sys.argv[5]
boa_peaks_file_name = sys.argv[6]
peaks_file_name = sys.argv[7]

SAN_write = open(SAN_file_name, "w")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")
boa_peaks_write = open(boa_peaks_file_name, "w")
boa_peaks_write.write("id,boa_peak,boa_size\n")
peaks_write = open(peaks_file_name, "w")


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

def get_nth_ascent(neighbors, n):
  neighbors_descending = list()
  for i in range(0, len(neighbors)):
    #score = fitness(np.array(int2bits(neighbors[i], N), dtype=bool), contrs, fit_mem)
    score = fitness(neighbors[i])
    scored_neighbor = (neighbors[i], score)
    j = 0
    while j < len(neighbors_descending):
      if scored_neighbor[1] < neighbors_descending[j][1]:
        j += 1
      else:
        break
    neighbors_descending.insert(j, scored_neighbor)
  return neighbors_descending[n-1][0]

'''Union_Find_methods'''
def find(p, q):
  return root(p) == root(q)
                                                                  
def unite(p, q, peak):
  i = root(p)
  j = root(q)
  boa_uf[i] = j
  #Add code for peak consideration for root
  '''
  if p == peak:
    boa_uf[i] = p
    boa_uf[j] = p
    boa_uf[p] = p
    boa_uf[q] = p
    size_uf[j] += size_uf[i]
    elif size_uf[i] < size_uf[j]:
                                                                                                                    
    if size_uf[i] < size_uf[j]:
      boa_uf[i] = j
      size_uf[j] += size_uf[i]
    else:
      boa_uf[j] = i
      size_uf[i] += size_uf[j]
    '''

def root(p):
  while p != boa_uf[p]:
    boa_uf[p] = boa_uf[boa_uf[p]]
    p = boa_uf[p]
  return p

#contrs = gen_contrs(N, K)
max_num = -1
max_fit = 0

steps = list()
all_fitnesses = list()
peaks = list()
boa_sizes = dict()

for i in range(0,num_points):
#  fit = fitness(np.array(int2bits(i, N), dtype=bool), contrs, fit_mem)
  fit = fitness(i)
  all_fitnesses.append((i, fit))
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, base)
  nth_neighbor = get_nth_ascent(neighbors, n)
  edge = str(i) + ";" + str(nth_neighbor)
  steps.append(edge)

  if (i == nth_neighbor):
#    print("i = " + str(i) + " and steepest neighbor = " + str(nth_neighbor))
#unite(i, nth_neighbor, i)
    peaks.append(i)
#    print(root(i))

  if not find(i, nth_neighbor):
    unite(i, nth_neighbor, -1)

#  print(str(boa_uf) + "\n" + str(i) + "\n" + str(nth_neighbor)) 

  if i % 50000 == 0:
    print("Processed: " + str(i))


for item in steps:
  SAN_write.write(item + "\n")

for fitness in all_fitnesses:
  fit_write.write(str(fitness[0]) + "," + str(fitness[1]) + "\n")

#compile counts for boa sizes
for i in range(0, len(boa_uf)):
  if root(i) in boa_sizes:
    boa_sizes[root(i)] += 1
  else:
    boa_sizes[root(i)] = 1

for i in range(0, len(boa_uf)):
  boa_peaks_write.write(str(i) + "," + str(root(i)) + "," + str(boa_sizes[root(i)]) +"\n")
#  print(str(i) + " has root: " + str(root(i)))

for peak in peaks:
  peaks_write.write(str(peak) + "\n")



'''
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
'''


print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
