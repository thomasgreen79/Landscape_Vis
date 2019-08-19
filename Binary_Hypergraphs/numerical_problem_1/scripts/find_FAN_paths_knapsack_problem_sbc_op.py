'''
Script for generating numerical 1 FAN Landscape.
Based on the equation: y = ((x/1300)-6)^3 - ((x/650)-3)**2 + 250 
which has one peak in the range [0,16384] making this a simple
numerical problem in Cartesian space. When searched as a binary
representation of integer values in the same range the number of
peaks increases to ... but is still relatively simple.
'''

import sys, queue
import numpy as np
from numpy import random

np.random.seed(19)

if len(sys.argv) < 5:
  print("Usage: python find_FAN_paths_numerical_problem_1_sbc_op.py <network_output_filename.csv> <fitness_output_filename.csv> <boa_peaks_filename.csv> <peaks_filename.txt>")
  sys.exit(0)


base = 14
num_points = 2**base

sys.setrecursionlimit(num_points)


'''Usage

    **Output file_names are expected input to run script.**

After calculating the First Ascent Network of the given search problem Fitness Landscape,
various data is output to files used when creating the jsons used for visualization.

1. Full egde-list of FAN FL as semicolon separated triplets
2. List of nodes and their fitness values
3. List of nodes and the peaks of their FAN Basins of Attraction, with size of each BOA listed
4. List of all peaks
'''

'''Code'''
#File names from command line
FAN_file_name = sys.argv[1]
fit_file_name = sys.argv[2]
boa_peaks_file_name = sys.argv[3]
peaks_file_name = sys.argv[4]

#writer objects for each file name
FAN_write = open(FAN_file_name, "w")
FAN_write.write("Source;Target;Weight\n")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")
boa_peaks_write = open(boa_peaks_file_name, "w")
boa_peaks_write.write("id;boa_list;boa_size\n")
peaks_write = open(peaks_file_name, "w")

#Functions
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

def calc_FA_probs(neighbors, node_id):
  node_fit = fitness(node_id)
  neighbors_improved = dict()
  num_improved = 0
  best_index = 0
  best_fit = node_fit
  for i in range(0, len(neighbors)):
    neighbor_fit = fitness(neighbors[i])
    if neighbor_fit >= best_fit:
      best_index = i
      best_fit = neighbor_fit
    if neighbor_fit > node_fit:
      num_improved += 1
      neighbors_improved[neighbors[i]] = 1
    else:
      neighbors_improved[neighbors[i]] = 0
  '''Break down what's happening here to find edge cases (peak with 0 fitness...)
  when porting code to Java
  '''
  if num_improved > 0:
    for i in range(0, len(neighbors)):
      neighbors_improved[neighbors[i]] = float(neighbors_improved[neighbors[i]])/num_improved
  neighbor_probs[node_id] = neighbors_improved
  return neighbors[best_index]

def calc_boa_of_peak(peak):
  que = queue.Queue()
  basin = list()
  already_seen = list()
  neighbors = get_neighbors(peak, base)
  for neighbor in neighbors:
    if fitness(neighbor) < fitness(peak):
      que.put(neighbor)
      already_seen.append(neighbor)
  calc_boa_recurs(peak, que, basin, already_seen)
  return basin

def calc_boa_recurs(peak, que, basin, already_seen):
  while not que.empty():
    next_node = que.get()
    basin.append(next_node)
    next_node_neighbors = get_neighbors(next_node, base)
    for next_node_neighbor in next_node_neighbors:
      if fitness(next_node_neighbor) < fitness(next_node) and next_node_neighbor not in already_seen:
        que.put(next_node_neighbor)
        already_seen.append(next_node_neighbor)
    calc_boa_recurs(next_node, que, basin, already_seen)

'''-----------------------------------------------------------------------------------------------'''


###Script Start###

max_num = -1
max_fit = 0
neighbor_probs = dict()
all_fitnesses = list()
peaks = list()
boas = dict()


#=== Calculating First Ascent of FL ===#

for i in range(0,num_points):
  fit = fitness(i)
  all_fitnesses.append((i, fit))	#Track fitnesses
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, base)
  best_neighbor = calc_FA_probs(neighbors, i)
  
  if (i == best_neighbor):
    peaks.append(i)			#Track peaks

  if i % 50000 == 0:
    print("Processed: " + str(i))

#=== Calculating BOA of First Ascent Network ===#

for peak in peaks:
  basin = calc_boa_of_peak(peak)
  boas[peak] = basin

#=== Output of First Ascent Network edge probabilities ===#
'''Break down what's happening here to find edge cases (peak with 0 fitness...)
when porting code to Java
'''
for node_id in neighbor_probs:
  for neighbor_id in neighbor_probs[node_id]:
    if neighbor_probs[node_id][neighbor_id] > 0:
      FAN_write.write(str(node_id) + ";" + str(neighbor_id) + ";" + str(neighbor_probs[node_id][neighbor_id]) + "\n")

#=== Output of Calculated First Ascent Values ===#

for fitness in all_fitnesses:
  fit_write.write(str(fitness[0]) + "," + str(fitness[1]) + "\n")

for peak in peaks:
  peaks_write.write(str(peak) + "\n")


for boa_peak in boas:
  boa_peaks_write.write(str(boa_peak) + ";" + str(boas[boa_peak]) + ";" + str(len(boas[boa_peak])) + "\n")
  

#Finishing output
print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
