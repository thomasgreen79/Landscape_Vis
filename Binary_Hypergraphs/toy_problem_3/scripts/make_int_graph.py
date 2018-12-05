import math

for i in range(71):
  print(str(i) + "," + str(abs(math.exp(i**(1.0/3.0))*math.sin(i))))
