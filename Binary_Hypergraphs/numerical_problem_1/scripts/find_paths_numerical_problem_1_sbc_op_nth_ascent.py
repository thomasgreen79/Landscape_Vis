'''
Using a numerical problem search space, find the nth biggest ascent of an sbc operator from every point in the landscape and write
links of the resulting network to an output network csv file,
fitnesses of every node to an output fitness csv file,
peaks of each Basin of Attraction from every node to an output BoA csv file,
list of all peaks to an output peaks csv file.
'''

import sys
import numpy as np
from numpy import random
from ast import literal_eval as make_tuple
from decimal import *

np.random.seed(19)

if len(sys.argv) < 7:
  print("Usage: python find_paths_numerical_problem_sbc_op.py <num_bits> <nth rank> <network_output_filename.csv> <fitness_output_filename.csv> <boa_peaks_filename.csv> <peaks_filename.txt>")
  sys.exit(0)

num_bits = int(sys.argv[1])
n = int(sys.argv[2])

if n < 1 or n > num_bits:
  print("Nth Ascent ranking must be between 1 and the number of neighbors (inclusive)")
  sys.exit()

num_points = 2**num_bits

#Adding two lists for UF code for Basin of Attraction data
boa_uf = list()
size_uf = list()

#Initialize Union Find "arrays"
for i in range(0,num_points):
  boa_uf.append(i)
  size_uf.append(1)

SAN_file_name = sys.argv[3]
fit_file_name = sys.argv[4]
boa_peaks_file_name = sys.argv[5]
peaks_file_name = sys.argv[6]

SAN_write = open(SAN_file_name, "w")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")
boa_peaks_write = open(boa_peaks_file_name, "w")
boa_peaks_write.write("id,boa_peak,boa_size\n")
peaks_write = open(peaks_file_name, "w")

def fitness(val):
  return ((val/1300)-6)**3-((val/650)-3)**2+250
  
def flip_bit(value, bit_index):
  value ^= (1 << bit_index)
  return value

def get_neighbors(vert_id, num_neighbors):
  neighbors = list()
  neighbors.append(vert_id)
  for i in range(0,num_neighbors):
    neighbors.append(flip_bit(vert_id, i))
  return neighbors

'''Choose the nth biggest neighbor where n ranges from 1 to num neighbors'''
def get_nth_ascent(neighbors, n):
  neighbors_descending = list()
  for i in range(0, len(neighbors)):
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
  fit = fitness(i)
  all_fitnesses.append((i, fit))
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, num_bits)
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

#  print(str(fit_mem))
#print(peaks)

print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
