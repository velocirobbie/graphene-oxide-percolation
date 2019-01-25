import sys
from histogram import Histogram
import numpy as np
from bootstrap import Bootstrap_method

with open('radii.dat','r') as f:
    N = 0
    for line in f:
        N += 1
    f.seek(0)
    bins = len(f.readline().split())
    f.seek(0)
    radii = np.zeros((bins,N))
    
    for i,line in enumerate(f):
        for j,r in enumerate(line.split()):
            radii[j,i] = float(r)
    
    hist = []

#for i in range(N):
#    B = Bootstrap_method(coverages[:,i])
#    conf = B.conf_interval(95)
#    print 2**i, B.mean, conf[0], conf[1]

#for i in range(N):
#    a = Histogram(coverages[:,i],resolution=50,range_=[0,1])
#    a.normalise()
#    hist += [a.hist[:,1]]
with open('rad.dat','w') as f:
    for i in radii:
        for j in i:
            f.write(str(j)+'\t')
        f.write('\n')
#    for i,subhist in enumerate(np.transpose(hist)):
#        f.write(str(a.hist[i,0])+'\t')
#        for j in subhist:
#            f.write(str(j)+'\t')
#        f.write('\n')

