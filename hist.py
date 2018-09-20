import sys
sys.path.append('/Users/robertsinclair/python_bin/')
from histogram import Histogram
import numpy as np
from bootstrap import Bootstrap_method

with open('coverages.dat','r') as f:
    N = 0
    for line in f:
        N += 1
    f.seek(0)
    Nrates = len(f.readline().split())
    f.seek(0)
    coverages = np.zeros((Nrates,N))
    
    for i,line in enumerate(f):
        for j,coverage in enumerate(line.split()):
            coverages[j,i] = float(coverage)
    
    hist = []

for i in range(N):
    B = Bootstrap_method(coverages[:,i])
    conf = B.conf_interval(95)
    print 2**i, B.mean, conf[0], conf[1]

for i in range(N):
    a = Histogram(coverages[:,i],resolution=50,range_=[0,1])
    a.normalise()
    hist += [a.hist[:,1]]
with open('hist.dat','w') as f:
    for i,subhist in enumerate(np.transpose(hist)):
        f.write(str(a.hist[i,0])+'\t')
        for j in subhist:
            f.write(str(j)+'\t')
        f.write('\n')

