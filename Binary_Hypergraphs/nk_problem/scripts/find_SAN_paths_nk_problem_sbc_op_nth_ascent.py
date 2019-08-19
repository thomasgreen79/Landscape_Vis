'''
Using an N,K problem search space, find the nth biggest ascent of an sbc operator from every point in the landscape and write
links of the resulting network to an output network csv file,
fitnesses of every node to an output fitness csv file,
peaks of each Basin of Attraction from every node to an output BoA csv file,
list of all peaks to an output peaks csv file.
The Fitness Memory of points is either to be read in, if it exists, or written out if this is the first problem of these N,K values.
'''

import sys, re
import numpy as np
from numpy import random
from ast import literal_eval as make_tuple
from decimal import *

np.random.seed(13)

if len(sys.argv) < 11:
  print("Usage: python find_paths_nk_problem_sbc_op.py <N> <K> <nth rank> <network_output_filename.csv> <fitness_output_filename.csv> <boa_peaks_filename.csv> <peaks_filename.txt> <read or write: 'r' or 'w'> <fit_mem_filename.txt> <contribs_filename.txt>")
  sys.exit(0)

N = int(sys.argv[1])
K = int(sys.argv[2])
n = int(sys.argv[3])

fit_mem = {}
contrs = {}

if n < 1 or n > N:
  print("Nth Ascent ranking must be between 1 and the number of neighbors (inclusive)")
  sys.exit()

num_points = 2**N

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
read_or_write = sys.argv[8]
fit_mem_file_name = sys.argv[9]
contribs_file_name = sys.argv[10]

SAN_write = open(SAN_file_name, "w")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")
boa_peaks_write = open(boa_peaks_file_name, "w")
boa_peaks_write.write("id,boa_peak,boa_size\n")
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

'''Choose the nth biggest neighbor where n ranges from 1 to num neighbors'''
def get_nth_ascent(neighbors, n):
  neighbors_descending = list()
  for i in range(0, len(neighbors)):
    score = fitness(np.array(int2bits(neighbors[i], N), dtype=bool), contrs, fit_mem)
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




max_num = -1
max_fit = 0

steps = list()
all_fitnesses = list()
peaks = list()
boa_sizes = dict()


#=== Calculating Steepest Ascent of FL ===#

for i in range(0,num_points):
  fit = fitness(np.array(int2bits(i, N), dtype=bool), contrs, fit_mem)
  all_fitnesses.append((i, fit))
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, N)
  nth_neighbor = get_nth_ascent(neighbors, n)
  edge = str(i) + ";" + str(nth_neighbor)
  steps.append(edge)

  if (i == nth_neighbor):
    peaks.append(i)

  if not find(i, nth_neighbor):
    unite(i, nth_neighbor, -1)
 
  if i % 50000 == 0:
      print("Processed: " + str(i))

#=== Output of Steepest Ascent Network edges ===#

for item in steps:
  SAN_write.write(item + "\n")

#=== Output of Calculated Steepest Ascent Values ===#

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

for peak in peaks:
  peaks_write.write(str(peak) + "\n")

#=== Process fitness memory and contributions if write mode ===#

if read_or_write is 'w':
  write_fit_mem_to_file()
  write_contribs_to_file()

print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
