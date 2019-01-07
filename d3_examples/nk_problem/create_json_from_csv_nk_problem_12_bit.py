import sys
import numpy as np
from numpy import random


np.random.seed(19)

N = 12
K = 3
num_points = 2**N
'''
#NK setup for N = 12, K = 0
contrs = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9], 10: [10], 11: [11]}

fit_mem = {((0, False),): 0.8277605195977511, ((1, False),): 0.6182959736513846, ((2, False),): 0.1572666513354719, ((3, False),): 0.0726316154632426, ((4, False),): 0.1677958539792358, ((5, False),): 0.9458649005152958, ((6, False),): 0.6677993586477289, ((7, False),): 0.059452921123052005, ((8, False),): 0.484280819675345, ((9, False),): 0.5352813338318995, ((10, False),): 0.3048528675661306, ((11, False),): 0.6721723824381546, ((11, True),): 0.4158875105958394, ((10, True),): 0.4305845846853713, ((9, True),): 0.29883942158169585, ((8, True),): 0.9513678476389672, ((7, True),): 0.04041322439193773, ((6, True),): 0.6265622117252427, ((5, True),): 0.9029159781972637, ((4, True),): 0.8046186200977472, ((3, True),): 0.08343274015911895, ((2, True),): 0.032123355183715896, ((1, True),): 0.7107304255902954, ((0, True),): 0.0406821411797712}
'''

#NK setup for N = 12, K = 3
contrs = {0: [0, 7, 8, 10], 1: [1, 2, 6, 8], 2: [2, 6, 10, 11], 3: [0, 3, 6, 7], 4: [0, 1, 2, 4], 5: [5, 6, 7, 9], 6: [5, 6, 10, 11], 7: [3, 5, 6, 7], 8: [1, 6, 8, 11], 9: [1, 4, 9, 10], 10: [4, 9, 10, 11], 11: [2, 5, 8, 11]}

fit_mem = {((0, False), (6, False), (7, False), (8, False)): 0.0751065219875301, ((1, False), (2, False), (7, False), (9, False)): 0.694502566363789, ((0, False), (2, False), (5, False), (6, False)): 0.2962932397123158, ((1, False), (3, False), (4, False), (5, False)): 0.5347007737021375, ((1, False), (4, False), (5, False), (6, False)): 0.01586863555995288, ((0, False), (3, False), (5, False), (11, False)): 0.8606716086856411, ((0, False), (6, False), (8, False), (10, False)): 0.6356344851290656, ((3, False), (4, False), (7, False), (11, False)): 0.614579502282931, ((3, False), (6, False), (7, False), (8, False)): 0.9547385882416332, ((3, False), (7, False), (8, False), (9, False)): 0.3517497883089197, ((2, False), (4, False), (7, False), (10, False)): 0.7499961201997953, ((0, False), (1, False), (8, False), (11, False)): 0.6831626872429066, ((0, False), (3, False), (5, False), (11, True)): 0.9965864461490838, ((3, False), (4, False), (7, False), (11, True)): 0.9639070257584988, ((0, False), (1, False), (8, False), (11, True)): 0.6282651565508994, ((0, False), (6, False), (8, False), (10, True)): 0.32504357438848397, ((2, False), (4, False), (7, False), (10, True)): 0.05468787457248514, ((1, False), (2, False), (7, False), (9, True)): 0.18410207079146235, ((3, False), (7, False), (8, False), (9, True)): 0.2343577713976155, ((0, False), (6, False), (7, False), (8, True)): 0.8923189300649103, ((0, False), (6, False), (8, True), (10, False)): 0.36751648603525855, ((3, False), (6, False), (7, False), (8, True)): 0.2600042879536305, ((3, False), (7, False), (8, True), (9, False)): 0.1268130627517141, ((0, False), (1, False), (8, True), (11, False)): 0.8405364804293797, ((0, False), (1, False), (8, True), (11, True)): 0.7259764873926902, ((0, False), (6, False), (8, True), (10, True)): 0.7564026939752138, ((3, False), (7, False), (8, True), (9, True)): 0.5435214782582534, ((0, False), (6, False), (7, True), (8, False)): 0.5574566839738962, ((1, False), (2, False), (7, True), (9, False)): 0.8755688555095706, ((3, False), (4, False), (7, True), (11, False)): 0.361292585972248, ((3, False), (6, False), (7, True), (8, False)): 0.07238225138150223, ((3, False), (7, True), (8, False), (9, False)): 0.8127857346473986, ((2, False), (4, False), (7, True), (10, False)): 0.09235109456545221, ((3, False), (4, False), (7, True), (11, True)): 0.1489038602688485, ((2, False), (4, False), (7, True), (10, True)): 0.5253060786853447, ((1, False), (2, False), (7, True), (9, True)): 0.16896881400842745, ((3, False), (7, True), (8, False), (9, True)): 0.7434790668694932, ((0, False), (6, False), (7, True), (8, True)): 0.45747835783225044, ((3, False), (6, False), (7, True), (8, True)): 0.29331395435813845, ((3, False), (7, True), (8, True), (9, False)): 0.9531017833026203, ((3, False), (7, True), (8, True), (9, True)): 0.8814259448363546, ((0, False), (6, True), (7, False), (8, False)): 0.2893376207029924, ((0, False), (2, False), (5, False), (6, True)): 0.6650776855843185, ((1, False), (4, False), (5, False), (6, True)): 0.5240759521096451, ((0, False), (6, True), (8, False), (10, False)): 0.028322568155863204, ((3, False), (6, True), (7, False), (8, False)): 0.5589416295014938, ((0, False), (6, True), (8, False), (10, True)): 0.06271160052866598, ((0, False), (6, True), (7, False), (8, True)): 0.8943819004958579, ((0, False), (6, True), (8, True), (10, False)): 0.6342087420219874, ((3, False), (6, True), (7, False), (8, True)): 0.6143731277898442, ((0, False), (6, True), (8, True), (10, True)): 0.45969004087960075, ((0, False), (6, True), (7, True), (8, False)): 0.7435369486001534, ((3, False), (6, True), (7, True), (8, False)): 0.42911191168832175, ((0, False), (6, True), (7, True), (8, True)): 0.6520040292795662, ((3, False), (6, True), (7, True), (8, True)): 0.08657924914319592, ((0, False), (2, False), (5, True), (6, False)): 0.9007768202223587, ((1, False), (3, False), (4, False), (5, True)): 0.7693323228079445, ((1, False), (4, False), (5, True), (6, False)): 0.4261146220148686, ((0, False), (3, False), (5, True), (11, False)): 0.12446548159694204, ((0, False), (3, False), (5, True), (11, True)): 0.5426374711829212, ((0, False), (2, False), (5, True), (6, True)): 0.6110478726472385, ((1, False), (4, False), (5, True), (6, True)): 0.7501995112471593, ((1, False), (3, False), (4, True), (5, False)): 0.3732003226034527, ((1, False), (4, True), (5, False), (6, False)): 0.0267026620967451, ((3, False), (4, True), (7, False), (11, False)): 0.11301200749066331, ((2, False), (4, True), (7, False), (10, False)): 0.7214279308251309, ((3, False), (4, True), (7, False), (11, True)): 0.8769474469404003, ((2, False), (4, True), (7, False), (10, True)): 0.04537950815510028, ((3, False), (4, True), (7, True), (11, False)): 0.3201546400094145, ((2, False), (4, True), (7, True), (10, False)): 0.7030584905427474, ((3, False), (4, True), (7, True), (11, True)): 0.5091207027752886, ((2, False), (4, True), (7, True), (10, True)): 0.2946571575101038, ((1, False), (4, True), (5, False), (6, True)): 0.09491332725419466, ((1, False), (3, False), (4, True), (5, True)): 0.09971475224558402, ((1, False), (4, True), (5, True), (6, False)): 0.11008674075265823, ((1, False), (4, True), (5, True), (6, True)): 0.7345913901960212, ((1, False), (3, True), (4, False), (5, False)): 0.9423627543164755, ((0, False), (3, True), (5, False), (11, False)): 0.9238717687619875, ((3, True), (4, False), (7, False), (11, False)): 0.6542010164666665, ((3, True), (6, False), (7, False), (8, False)): 0.8930778664067226, ((3, True), (7, False), (8, False), (9, False)): 0.6422421219787242, ((0, False), (3, True), (5, False), (11, True)): 0.4368248305776625, ((3, True), (4, False), (7, False), (11, True)): 0.6826314916543355, ((3, True), (7, False), (8, False), (9, True)): 0.26079824762387604, ((3, True), (6, False), (7, False), (8, True)): 0.7368968148955272, ((3, True), (7, False), (8, True), (9, False)): 0.7757286101823124, ((3, True), (7, False), (8, True), (9, True)): 0.46164094285479584, ((3, True), (4, False), (7, True), (11, False)): 0.6592578461170082, ((3, True), (6, False), (7, True), (8, False)): 0.0375568407965966, ((3, True), (7, True), (8, False), (9, False)): 0.2294441091394671, ((3, True), (4, False), (7, True), (11, True)): 0.4248458022378918, ((3, True), (7, True), (8, False), (9, True)): 0.10526216920967246, ((3, True), (6, False), (7, True), (8, True)): 0.5715162972312734, ((3, True), (7, True), (8, True), (9, False)): 0.22872136550743594, ((3, True), (7, True), (8, True), (9, True)): 0.8050330380451849, ((3, True), (6, True), (7, False), (8, False)): 0.2761554760853092, ((3, True), (6, True), (7, False), (8, True)): 0.37977759527748, ((3, True), (6, True), (7, True), (8, False)): 0.3760246460487253, ((3, True), (6, True), (7, True), (8, True)): 0.9709357361306298, ((1, False), (3, True), (4, False), (5, True)): 0.8077210264777321, ((0, False), (3, True), (5, True), (11, False)): 0.29213526344243834, ((0, False), (3, True), (5, True), (11, True)): 0.5945325062797273, ((1, False), (3, True), (4, True), (5, False)): 0.6773046149148509, ((3, True), (4, True), (7, False), (11, False)): 0.9878696776571003, ((3, True), (4, True), (7, False), (11, True)): 0.9003520700989857, ((3, True), (4, True), (7, True), (11, False)): 0.9788971969394986, ((3, True), (4, True), (7, True), (11, True)): 0.8791274426525582, ((1, False), (3, True), (4, True), (5, True)): 0.42641585598382825, ((1, False), (2, True), (7, False), (9, False)): 0.760973242873649, ((0, False), (2, True), (5, False), (6, False)): 0.26467785360902885, ((2, True), (4, False), (7, False), (10, False)): 0.2304130228936515, ((2, True), (4, False), (7, False), (10, True)): 0.5896761410732534, ((1, False), (2, True), (7, False), (9, True)): 0.589741409898443, ((1, False), (2, True), (7, True), (9, False)): 0.6926749645022847, ((2, True), (4, False), (7, True), (10, False)): 0.2217195384840629, ((2, True), (4, False), (7, True), (10, True)): 0.6334419704258001, ((1, False), (2, True), (7, True), (9, True)): 0.6819662996710084, ((0, False), (2, True), (5, False), (6, True)): 0.5420009689878745, ((0, False), (2, True), (5, True), (6, False)): 0.9195348329708438, ((0, False), (2, True), (5, True), (6, True)): 0.06493929448375713, ((2, True), (4, True), (7, False), (10, False)): 0.8879402469068349, ((2, True), (4, True), (7, False), (10, True)): 0.18625582733108637, ((2, True), (4, True), (7, True), (10, False)): 0.4292006098927369, ((2, True), (4, True), (7, True), (10, True)): 0.3385178701007814, ((1, True), (2, False), (7, False), (9, False)): 0.18580449416939426, ((1, True), (3, False), (4, False), (5, False)): 0.5013730094329695, ((1, True), (4, False), (5, False), (6, False)): 0.14087424467271226, ((0, False), (1, True), (8, False), (11, False)): 0.619827289452755, ((0, False), (1, True), (8, False), (11, True)): 0.674104951768581, ((1, True), (2, False), (7, False), (9, True)): 0.4816794464634634, ((0, False), (1, True), (8, True), (11, False)): 0.16210793005400403, ((0, False), (1, True), (8, True), (11, True)): 0.5249693265493064, ((1, True), (2, False), (7, True), (9, False)): 0.21243832631985038, ((1, True), (2, False), (7, True), (9, True)): 0.3642288136528061, ((1, True), (4, False), (5, False), (6, True)): 0.07607775474772038, ((1, True), (3, False), (4, False), (5, True)): 0.7030419856362927, ((1, True), (4, False), (5, True), (6, False)): 0.5209790442884025, ((1, True), (4, False), (5, True), (6, True)): 0.3602193814069742, ((1, True), (3, False), (4, True), (5, False)): 0.2692321484686838, ((1, True), (4, True), (5, False), (6, False)): 0.6340079059165636, ((1, True), (4, True), (5, False), (6, True)): 0.9986431315128445, ((1, True), (3, False), (4, True), (5, True)): 0.9078170246432539, ((1, True), (4, True), (5, True), (6, False)): 0.27213012637423706, ((1, True), (4, True), (5, True), (6, True)): 0.7099320001873837, ((1, True), (3, True), (4, False), (5, False)): 0.9918303299269704, ((1, True), (3, True), (4, False), (5, True)): 0.6649157541507127, ((1, True), (3, True), (4, True), (5, False)): 0.06999502023326121, ((1, True), (3, True), (4, True), (5, True)): 0.2774613227125441, ((1, True), (2, True), (7, False), (9, False)): 0.0034792477666455435, ((1, True), (2, True), (7, False), (9, True)): 0.7074902376154918, ((1, True), (2, True), (7, True), (9, False)): 0.5404813858345667, ((1, True), (2, True), (7, True), (9, True)): 0.09828161629433407, ((0, True), (6, False), (7, False), (8, False)): 0.40942031783222765, ((0, True), (2, False), (5, False), (6, False)): 0.7137332587298815, ((0, True), (3, False), (5, False), (11, False)): 0.8638113617954597, ((0, True), (6, False), (8, False), (10, False)): 0.07566678087168643, ((0, True), (1, False), (8, False), (11, False)): 0.33989447075008905, ((0, True), (3, False), (5, False), (11, True)): 0.2874374258118003, ((0, True), (1, False), (8, False), (11, True)): 0.6349437810423518, ((0, True), (6, False), (8, False), (10, True)): 0.4667488461913748, ((0, True), (6, False), (7, False), (8, True)): 0.6202892949575771, ((0, True), (6, False), (8, True), (10, False)): 0.9164391851507504, ((0, True), (1, False), (8, True), (11, False)): 0.002461047673435246, ((0, True), (1, False), (8, True), (11, True)): 0.06296230546924597, ((0, True), (6, False), (8, True), (10, True)): 0.9378194846637368, ((0, True), (6, False), (7, True), (8, False)): 0.9695266367078947, ((0, True), (6, False), (7, True), (8, True)): 0.5226682559784872, ((0, True), (6, True), (7, False), (8, False)): 0.867972012092156, ((0, True), (2, False), (5, False), (6, True)): 0.877416578773382, ((0, True), (6, True), (8, False), (10, False)): 0.10330389742885482, ((0, True), (6, True), (8, False), (10, True)): 0.15156645694142312, ((0, True), (6, True), (7, False), (8, True)): 0.5656715532247728, ((0, True), (6, True), (8, True), (10, False)): 0.7418785264570216, ((0, True), (6, True), (8, True), (10, True)): 0.8570506769806975, ((0, True), (6, True), (7, True), (8, False)): 0.7672401938388421, ((0, True), (6, True), (7, True), (8, True)): 0.49805623466333715, ((0, True), (2, False), (5, True), (6, False)): 0.862671166330057, ((0, True), (3, False), (5, True), (11, False)): 0.18301160749336598, ((0, True), (3, False), (5, True), (11, True)): 0.8592514325951008, ((0, True), (2, False), (5, True), (6, True)): 0.006085370046004401, ((0, True), (3, True), (5, False), (11, False)): 0.9932245701272989, ((0, True), (3, True), (5, False), (11, True)): 0.6705507547260806, ((0, True), (3, True), (5, True), (11, False)): 0.19678728378205002, ((0, True), (3, True), (5, True), (11, True)): 0.21723095356012045, ((0, True), (2, True), (5, False), (6, False)): 0.2813802697555975, ((0, True), (2, True), (5, False), (6, True)): 0.9646436137014062, ((0, True), (2, True), (5, True), (6, False)): 0.986259892751048, ((0, True), (2, True), (5, True), (6, True)): 0.1752308502240647, ((0, True), (1, True), (8, False), (11, False)): 0.8953764346413737, ((0, True), (1, True), (8, False), (11, True)): 0.6996984416849801, ((0, True), (1, True), (8, True), (11, False)): 0.027766130314615833, ((0, True), (1, True), (8, True), (11, True)): 0.08286618963713277}


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
