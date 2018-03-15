from sim_backup import Sim
import numpy as np
#a = Sim(4,20)
import sys

size = [1000] #length of box
rates = [10**i for i in range(5)]
res  = 1
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
epoch = 10
for i in range(len(rates)):
    rfile = 'radii'+str(rates[i])
    cfile = 'cover'+str(rates[i])
    print rates[i] ,'--==='
    coverage = []
    for j in range(epoch):
        #if not j%100: print j
        a = Sim(rates[i],1000, res,Nmonte_points=1000,graph=True)
        a.simulate()
        coverage += [a.coverage]
#        a.print_output()
    print np.sum(coverage)/epoch, np.std(coverage)
#     with open(rfile,'a') as f:
#         for r in a.radii:
#             f.write(str(r)+'\t')
#         f.write('\n')
#     with open(cfile,'a') as f:
#         f.write(str(a.coverage)+'\n')
#    for r in a.radii:
#        r_xbin = int( float(r) * rhists#ize / size )
#        rhist[r_xbin][i] += 1.0/len(a.radii)
#    c_bin = int( float(a.coverage) * chistsize )
#    chist[c_bin][i] += 1
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
