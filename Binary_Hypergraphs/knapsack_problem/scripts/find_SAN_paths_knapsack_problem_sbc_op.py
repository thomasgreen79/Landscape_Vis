'''
Script for generating knapsack Landscape with a specific set of weights and values.
The chosen set has no significance other than weights vals are all approximately
5x-10x the values vals to keep them relatively of equal likelihood to be chosen
given a search, and no weights are identical.
'''

import sys, math, re
import numpy as np
from numpy import random

np.random.seed(5974)

if len(sys.argv) < 14:
  print("Usage: python find_SAN_paths_knapsack_problem_sbc_op.py <num_elements> <max_tot_weight_percent> <nth rank> <min_weight> <max_weight> <min_multiplier> <max_multiplier> <network_output_filename.csv> <fitness_output_filename.csv> <boa_peaks_filename.csv> <peaks_filename.txt> <read or write: 'r' or 'w'> <wts_vals_filename.txt>")
  sys.exit(0)


base = int(sys.argv[1])
num_points = 2**base
max_wt_per = float(sys.argv[2])
W = 0
n = int(sys.argv[3])
min_wt = int(sys.argv[4])
max_wt = int(sys.argv[5])
min_mult = int(sys.argv[6])
max_mult = int(sys.argv[7])

wt = list()
val = list()

#Adding two lists for UF code for Basin of Attraction data
boa_uf = list()
size_uf = list()

#Initialize Union Find "arrays"
for i in range(0,num_points):
  boa_uf.append(i)
  size_uf.append(1)


'''Usage

    **Output file_names are expected input to run script.**

After calculating the Steepest Ascent Network of the given search problem Fitness Landscape,
various data is output to files used when creating the jsons used for visualization.

1. Full egde-list of SAN FL as semicolon separated pairs
2. List of nodes and their fitness values
3. List of nodes and the peaks of their SAN Basins of Attraction, with size of each BOA listed
4. List of all peaks
'''

'''Code'''
#File names from command line
SAN_file_name = sys.argv[8]
fit_file_name = sys.argv[9]
boa_peaks_file_name = sys.argv[10]
peaks_file_name = sys.argv[11]
read_or_write = sys.argv[12]
wts_vals_file_name = sys.argv[13]

#writer objects for each file name
SAN_write = open(SAN_file_name, "w")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")
boa_peaks_write = open(boa_peaks_file_name, "w")
boa_peaks_write.write("id,boa_peak,boa_size\n")
peaks_write = open(peaks_file_name, "w")
wts_vals_process = None

def read_wts_vals_from_file():
#Adjust process to handle read wts and vals instead
  wts_line = wts_vals_process.readline().strip()
  vals_line = wts_vals_process.readline().strip()
  wt = list(int(x) for x in re.sub('\[|\]', '', wts_line).split(' '))
  val = list(int(x) for x in re.sub('\[|\]', '', vals_line).split(' '))

def write_wts_vals_to_file():
  wts_vals_process.write("[")
  for i in range(0, len(wt)):
    wts_vals_process.write(str(wt[i]))
    if i == len(wt)-1:
      wts_vals_process.write("")
    else:
      wts_vals_process.write(" ")
  wts_vals_process.write("]\n")
  wts_vals_process.write("[")
  for i in range(0, len(val)):
    wts_vals_process.write(str(val[i]))
    if i == len(wt)-1:
      wts_vals_process.write("")
    else:
      wts_vals_process.write(" ")
  wts_vals_process.write("]\n")

if read_or_write == "r":
  wts_vals_process = open(wts_vals_file_name, "r")
  read_wts_vals_from_file()
elif read_or_write == "w":
  wts_vals_process = open(wts_vals_file_name, "w")
else:
  print("Weights and Values file error message")
  sys.exit(1)


#Functions
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

def get_nth_ascent(neighbors, n):	###Remove n, and rewrite as steepest (or first..)###
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

def generate_weights_and_vals():
  np_wts = np.random.randint(min_wt, max_wt, base)
  vals = list()
  for i in range(0, len(np_wts)):
    vals.append(math.ceil(np_wts[i]*(np.random.sample()*(max_mult-min_mult)+min_mult)))
  np_vals = np.array(vals)
  W = math.ceil(max_wt_per * sum(np_wts))
  return np_wts, np_vals, W

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


'''-----------------------------------------------------------------------------------------------'''


###Script Start###

max_num = -1
max_fit = 0
steps = list()
all_fitnesses = list()
peaks = list()
boa_sizes = dict()

wt, val, W = generate_weights_and_vals()

#=== Calculating Steepest Ascent of FL ===#

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



#=== Output of Calculated Steepest Ascent Values ===#

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


'''Likely old code..'''

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

#=== Process weights and values if write mode ===#

if read_or_write is 'w':
  write_wts_vals_to_file()

#Finishing output
print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
