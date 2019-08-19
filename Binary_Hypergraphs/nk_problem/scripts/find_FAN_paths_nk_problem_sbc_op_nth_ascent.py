'''
Using an N,K problem search space, find the nth biggest ascent of an sbc operator from every point in the landscape and write
links of the resulting network to an output network csv file,
fitnesses of every node to an output fitness csv file,
peaks of each Basin of Attraction from every node to an output BoA csv file,
list of all peaks to an output peaks csv file.
The Fitness Memory of points is either to be read in, if it exists, or written out if this is the first problem of these N,K values.
'''

import sys, re, queue
import numpy as np
from numpy import random
from ast import literal_eval as make_tuple
from decimal import *

np.random.seed(13)

if len(sys.argv) < 11:
  print("Usage: python find_paths_nk_problem_sbc_op.py <N> <K> <nth rank> <network_output_filename.csv> <fitness_output_filename.csv> <boa_peaks_filename.csv> <peaks_filename.txt> <read or write: 'r' or 'w'> <fit_mem_filename.csv> <contribs_filename.csv>")
  sys.exit(0)

N = int(sys.argv[1])
K = int(sys.argv[2])
n = int(sys.argv[3])
num_points = 2**N

sys.setrecursionlimit(num_points)

fit_mem = {}
contrs = {}

if n < 1 or n > N:
  print("Nth Ascent ranking must be between 1 and the number of neighbors (inclusive)")
  sys.exit()

#Adding two lists for UF code for Basin of Attraction data
boa_uf = list()
size_uf = list()

#Initialize Union Find "arrays"
for i in range(0,num_points):
  boa_uf.append(i)
  size_uf.append(1)

FAN_file_name = sys.argv[4]
fit_file_name = sys.argv[5]
boa_peaks_file_name = sys.argv[6]
peaks_file_name = sys.argv[7]
read_or_write = sys.argv[8]
fit_mem_file_name = sys.argv[9]
contribs_file_name = sys.argv[10]

FAN_write = open(FAN_file_name, "w")
FAN_write.write("Source;Target;Weight\n")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")
boa_peaks_write = open(boa_peaks_file_name, "w")
boa_peaks_write.write("id,boa_list,boa_size\n")
peaks_write = open(peaks_file_name, "w")
fit_mem_process = None
contribs_process = None


def read_fit_mem_from_file(fit_mem):
  while True:
    key_line = fit_mem_process.readline().strip()
    value_line = fit_mem_process.readline().strip()
    if not value_line:
      break
    fit_mem[make_tuple(key_line)] = float(value_line)

def write_fit_mem_to_file():
  for key in sorted(fit_mem):
    fit_mem_process.write(str(key) + "\n" + str(Decimal(fit_mem[key])) + "\n")

def read_contribs_from_file(contrs):
  while True:
    key_line = contribs_process.readline().strip()
    value_line = contribs_process.readline().strip()
    if not value_line:
      break
    contrs[int(key_line)] = list(int(x) for x in re.sub('\[|\]| ', '', value_line).split(','))

def write_contribs_to_file():
  for key in sorted(contrs):
    contribs_process.write(str(key) + "\n" + str(contrs[key]) + "\n")

def gen_contrs(n, k):
  contrs_temp = {}
  for i in range(0, n):
    contr_i_list = list()
    for j in range(0, k):
      possible_contr = np.random.randint(n)
      while possible_contr in contr_i_list or possible_contr == i:
        possible_contr = np.random.randint(n)
      contr_i_list.append(possible_contr)
    contr_i_list.append(i)
    contrs_temp[i] = contr_i_list
  return contrs_temp


if read_or_write == "r":
  getcontext().prec = 15
  fit_mem_process = open(fit_mem_file_name, "r")
  contribs_process = open(contribs_file_name, "r")
  read_fit_mem_from_file(fit_mem)
  read_contribs_from_file(contrs)
elif read_or_write == "w":
  fit_mem_process = open(fit_mem_file_name, "w")
  contribs_process = open(contribs_file_name, "w")
  contrs = gen_contrs(N, K)
else:
  print("Fit mem file error message")
  sys.exit(1)



def fitness_i(genotype, i, contribs, mem):
  key = tuple(zip(contribs[i], genotype[contribs[i]]))
  if key not in mem:
    mem[key] = np.random.uniform(0, 1)
  return mem[key]

def fitness(genotype, contribs, mem):
  return np.mean([fitness_i(genotype, i, contribs, mem) for i in range(len(genotype))])

def int2bits(k, N):
  x = list(map(int, bin(k)[2:]))
  pad = N - len(x)
  x = [0]*pad + x
  return x

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
  node_fit = fitness(np.array(int2bits(node_id, N), dtype=bool), contrs, fit_mem)
#  node_fit = fitness(node_id)
  neighbors_improved = dict()
  num_improved = 0
  best_index = 0
  best_fit = node_fit
  for i in range(0, len(neighbors)):
    neighbor_fit = fitness(np.array(int2bits(neighbors[i], N), dtype=bool), contrs, fit_mem)
#    neighbor_fit = fitness(neighbors[i])
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
  neighbors = get_neighbors(peak, N)
  for neighbor in neighbors:
    if fitness(np.array(int2bits(neighbor, N), dtype=bool), contrs, fit_mem) < fitness(np.array(int2bits(peak, N), dtype=bool), contrs, fit_mem):
      que.put(neighbor)
      already_seen.append(neighbor)
  calc_boa_recurs(peak, que, basin, already_seen)
  return basin

def calc_boa_recurs(peak, que, basin, already_seen):
  while not que.empty():
    next_node = que.get()
    basin.append(next_node)
    next_node_neighbors = get_neighbors(next_node, N)
    for next_node_neighbor in next_node_neighbors:
      if fitness(np.array(int2bits(next_node_neighbor, N), dtype=bool), contrs, fit_mem) < fitness(np.array(int2bits(next_node, N), dtype=bool), contrs, fit_mem) and next_node_neighbor not in already_seen:
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


#=== Calculating Steepest Ascent of FL ===#

for i in range(0,num_points):
  fit = fitness(np.array(int2bits(i, N), dtype=bool), contrs, fit_mem)
  all_fitnesses.append((i, fit))	#Track fitnesses
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, N)
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

for node_id in neighbor_probs:
  for neighbor_id in neighbor_probs[node_id]:
    if neighbor_probs[node_id][neighbor_id] > 0:
      FAN_write.write(str(node_id) + ";" + str(neighbor_id) + ";" + str(neighbor_probs[node_id][neighbor_id]) + "\n")

#=== Output of Calculated Steepest Ascent Values ===#

for fitness in all_fitnesses:
  fit_write.write(str(fitness[0]) + "," + str(fitness[1]) + "\n")

for peak in peaks:
  peaks_write.write(str(peak) + "\n")

for boa_peak in boas:
  boa_peaks_write.write(str(boa_peak) + ";" + str(boas[boa_peak]) + ";" + str(len(boas[boa_peak])) + "\n")

#=== Process fitness memory and contributions if write mode ===#

if read_or_write is 'w':
  write_fit_mem_to_file()
  write_contribs_to_file()

#Finishing output
print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
