import sys
from scipy.optimize import curve_fit
from scipy.special import gamma
from bootstrap import Bootstrap_method
import numpy as np
import sys


def beta(x, a, b):
    bottom = gamma(a)*gamma(b) / gamma(a+b)
    top = x**(a-1) * (1-x)**(b-1)
    return top / bottom

def beta_mean(a,b):
    return a/(a+b)

def beta_var(a,b):
    return a*b / ( (a + b)**2 * (a + b + 1) )

def calc_beta(a,b):
    res = 1000
    return beta(np.arange(0,1,1.0/res),a,b)

with open(sys.argv[1],'r') as f:
    count = 0
    for line in f:
        N = len(line.split()) - 1
        count += 1
    x = np.zeros(count)
    ys = np.zeros((count,N))
    f.seek(0)
    for i,line in enumerate(f):
        line = line.split()
        x[i] = float(line[0])
        ys[i] = [float(p) for p in line[1:]]

res = 1000

fit = np.zeros((N,res))
for i in range(N):
    param, conv = curve_fit(beta, x, ys[:,i])
    a = param[0]
    b = param[1]
    fit[i] = calc_beta(a,b)
    #print 2**i,beta_mean(a,b),beta_var(a,b)

with open('fit_coverage.dat','w') as f:
    res = len(fit[0])
    x = np.arange(0,1,1.0/res)
    for i, subfit in enumerate(fit.transpose()):
        f.write(str(x[i])+'\t')
        for j in subfit:
            f.write(str(j)+'\t')
        f.write('\n')



