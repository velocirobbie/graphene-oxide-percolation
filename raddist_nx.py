from sim import Sim
import numpy as np
#a = Sim(4,20)
import sys

N = 5
epoch = 100
size = 1000 #length of box
rates = [10**i for i in range(N)]
radii = np.empty((N,epoch))
coverage = np.empty((N,epoch))
res=1
"""
rhistsize = 50
rbinsize = size / rhistsize
rhist = np.zeros((rhistsize,len(rates)))
rbins = np.arange(rbinsize/2, rbinsize/2 + rhistsize*rbinsize, 
                  rbinsize)

chistsize = 50
cbinsize = 1.0 / chistsize
chist = np.zeros((chistsize, len(rates)))
cbins = np.arange(cbinsize/2, cbinsize/2 + chistsize*cbinsize,
                  cbinsize)
"""

np.random.seed(int(sys.argv[1]))
for i in range(N):
    print rates[i] ,'--==='
    for j in range(epoch):
        #if not j%100: print j
        a = Sim(rates[i], size, res,Nmonte_points=1000,graph=False)
        a.simulate()
#        a.print_output()
        coverage[i,j] = a.coverage
    print np.sum(coverage[i])/epoch, np.std(coverage[i])

with open('coveragees.dat','w') as f:
    for line in coverage:
        for i in line:
            f.write(str(i)+'\t')
        f.write('\n')

with open('radii.dat','w') as f:
    for line in radii:
        for i in line:
            f.write(str(i)+'\t')
        f.write('\n')
"""
with open('cover_hist','w') as f:
    for i in range(len(rhist)):
        f.write(str(cbins[i])+'\t')
        for j in range(len(rates)):
            f.write(str(chist[i][j])+'\t')
        f.write('\n')
with open('radial_hist','w') as f:
    for i in range(len(chist)):
        f.write(str(rbins[i])+'\t')
        for j in range(len(rates)):
            f.write(str(rhist[i][j])+'\t')
        f.write('\n')
"""
