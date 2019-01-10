import sys
import numpy as np
from numpy import random


np.random.seed(19)

N = 20
K = 3
num_points = 2**N
'''
#NK setup for N = 20, K = 0
contrs = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9], 10: [10], 11: [11], 12: [12], 13:[13], 14: [14], 15:[15], 16: [16], 17:[17], 18: [18], 19:[19]}

fit_mem = {((0, False),): 0.8277605195977511, ((1, False),): 0.6182959736513846, ((2, False),): 0.1572666513354719, ((3, False),): 0.0726316154632426, ((4, False),): 0.1677958539792358, ((5, False),): 0.9458649005152958, ((6, False),): 0.6677993586477289, ((7, False),): 0.059452921123052005, ((8, False),): 0.484280819675345, ((9, False),): 0.5352813338318995, ((10, False),): 0.3048528675661306, ((11, False),): 0.6721723824381546, ((12, False),): 0.09753360174945158, ((13, False),): 0.7612497166748563, ((14, False),): 0.24693797316632704, ((15, False),): 0.13813168747631954, ((16, False),): 0.33144656327093147, ((17, False),): 0.08299956500689287, ((18, False),): 0.6719770812804666, ((19, False),): 0.8065937981616575, ((19, True),): 0.982741914544214, ((18, True),): 0.6356607347968526, ((17, True),): 0.21592325604718032, ((16, True),): 0.5490274320842796, ((15, True),): 0.5455599580092261, ((14, True),): 0.23407607314700163, ((13, True),): 0.11372584300707944, ((12, True),): 0.4996592670489547, ((11, True),): 0.4158875105958394, ((10, True),): 0.4305845846853713, ((9, True),): 0.29883942158169585, ((8, True),): 0.9513678476389672, ((7, True),): 0.04041322439193773, ((6, True),): 0.6265622117252427, ((5, True),): 0.9029159781972637, ((4, True),): 0.8046186200977472, ((3, True),): 0.08343274015911895, ((2, True),): 0.032123355183715896, ((1, True),): 0.7107304255902954, ((0, True),): 0.0406821411797712}
'''

#NK setup for N = 20, K = 3
contrs = {0: [0, 1, 5, 10], 1: [1, 7, 12, 18], 2: [2, 7, 15, 16], 3: [3, 4, 9, 11], 4: [4, 5, 7, 17], 5: [2, 3, 5, 17], 6: [0, 4, 6, 17], 7: [7, 12, 17, 19], 8: [4, 8, 9, 11], 9: [0, 9, 10, 18], 10: [9, 10, 11, 16], 11: [1, 7, 11, 13], 12: [8, 9, 11, 12], 13: [1, 2, 6, 13], 14: [3, 10, 14, 16], 15: [9, 14, 15, 19], 16: [4, 5, 16, 19], 17: [1, 4, 12, 17], 18: [3, 9, 13, 18], 19: [6, 8, 12, 19]}

fit_mem = {}


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


csv_filename = sys.argv[1]
json_filename = sys.argv[2]

fr = open(csv_filename, "r")
fw = open(json_filename, "w")

nodes = list()
edges = dict()
fit_vals = list()

#max_fitness = 0.5705276904717379
max_fitness = 0.0

#add fitness value for each node
#find and set max fitness value

for line in fr:
  node_pair = line.strip().split(";")
  if node_pair[0] not in nodes:
    nodes.append(node_pair[0])
    fit_vals.append(fitness(np.array(int2bits(int(node_pair[0]), N), dtype=bool), contrs, fit_mem))
  if node_pair[1] not in nodes:
    nodes.append(node_pair[1])
    fit_vals.append(fitness(np.array(int2bits(int(node_pair[1]), N), dtype=bool), contrs, fit_mem))
  edge = (node_pair[0], node_pair[1])
  if edge not in edges:
    edges[edge] = 1
  else:
    edges[edge] = edges[edge] + 1

max_fitness = max(fit_vals)
print(max_fitness)

fw.write("{\n\"nodes\": [\n")
for i in range(0,len(nodes)):
#  print(str(fitness(int(nodes[i]))))
  fw.write("{\"id\":\"" + str(nodes[i]) + "\", \"group\":\"1\", \"fitness\":\"" + str(fitness(np.array(int2bits(int(nodes[i]), N), dtype=bool), contrs, fit_mem)/max_fitness) + "\"}")
  if i < len(nodes)-1:
    fw.write(",\n")
  else:
    fw.write("\n")

fw.write("],\n\"links\": [\n")
i = 0
for key in edges:
  if key[0] != key[1]:
    fw.write("{\"source\":\"" + str(key[0]) + "\", \"target\":\"" + str(key[1]) + "\", \"value\":\"" + str(edges[key]) + "\"}")
    if i < len(edges)-1:
      fw.write(",\n")
    else:
      fw.write("\n")
  i += 1
fw.write("]\n}\n")
