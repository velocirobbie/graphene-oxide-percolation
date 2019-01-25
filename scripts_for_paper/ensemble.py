from sim import Sim
import numpy as np
#a = Sim(4,20)
import sys

epoch = 1000
size = 1000 #length of box
Npoints = 10000
dr = 1/float(size)
rate = 2**float(sys.argv[1])
coverage = np.zeros((epoch))
errors   = np.zeros((epoch))
res=1

for j in range(epoch):
    #if not j%100: print j
    a = Sim(rate, dr, Nmonte_points= Npoints, graph=False, error=True)
    a.simulate()
    coverage[j] = a.corrected_coverage
    errors[j]   = a.error

with open('coverages.dat','a') as f:
    for i in coverage:
        f.write(str(i)+'\t')
    f.write('\n')

with open('errors.dat','w') as f:
    for i in errors:
        f.write(str(i)+'\t')
    f.write('\n')
