import sys
import numpy as np
from numpy import random

np.random.seed(19)

if len(sys.argv) < 4:
  print("Usage: python find_paths_nk_problem_sbc_op.py <N> <K> <network_output_filename.csv> <fitness_output_filenam.csv>")
  sys.exit(0)


N = int(sys.argv[1])
K = int(sys.argv[2])
num_points = 2**N

SAN_file_name = sys.argv[3]
fit_file_name = sys.argv[4]

SAN_write = open(SAN_file_name, "w")
fit_write = open(fit_file_name, "w")
fit_write.write("id,fitness\n")

contrs = {}
fit_mem = {}


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

def get_steepest_ascent(neighbors):
  max_ascent_index = -1
  max_ascent_value = -1
  for i in range(0, len(neighbors)):
    score = fitness(np.array(int2bits(neighbors[i], N), dtype=bool), contrs, fit_mem)
    if score > max_ascent_value:
      max_ascent_value = score
      max_ascent_index = i
  return neighbors[max_ascent_index]



contrs = gen_contrs(N, K)

max_num = -1
max_fit = 0
steps = list()
all_fitnesses = list()
for i in range(0,num_points):
  fit = fitness(np.array(int2bits(i, N), dtype=bool), contrs, fit_mem)
  all_fitnesses.append((i, fit))
  if fit > max_fit:
    max_fit = fit
    max_num = i

  neighbors = get_neighbors(i, N)
  best_neighbor = get_steepest_ascent(neighbors)
  edge = str(i) + ";" + str(best_neighbor)
  steps.append(edge)
  if i % 50000 == 0:
      print("Processed: " + str(i))


for item in steps:
  SAN_write.write(item + "\n")

for fitness in all_fitnesses:
  fit_write.write(str(fitness[0]) + "," + str(fitness[1]) + "\n")


print("max num is: " + str(max_num))
print("max fitness is: " + str(max_fit))
