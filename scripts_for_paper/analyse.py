from histogram import Histogram
import numpy as np
from bootstrap import Bootstrap_method

rates = [-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13] # directories to search
print 'rates',rates 
N = 1000 # replicas in each ensemble
coverages = np.zeros((N,len(rates)))
errors    = np.zeros((N,len(rates)))

# read in data
for i,rate in enumerate(rates):
    with open(str(rate)+'/coverages.dat','r') as f:
        line = f.readline()
        for j,coverage in enumerate(line.split()):
            coverages[j,i] = float(coverage)
    with open(str(rate)+'/errors.dat','r') as f:
        line = f.readline()
        for j,error in enumerate(line.split()):
            errors[j,i] = float(error)

# print average coverage, first and second standard deviations of distributions
for i in range(len(rates)):
    print rates[i],np.mean(coverages[:,i]), np.std(coverages[:,i]), np.std(coverages[:,i])*2

# average timestep error in an ensemble
with open('error.dat','w') as f:
    for i,rate in enumerate(rates):
        mean_error = np.mean(errors[:,i])
        f.write(str(rate)+'\t'+
                str(np.mean(coverages[:,i]))+'\t'+
                str(mean_error)+'\n')

# average coverage with 95% conf interval in the mean
for i,rate in enumerate(rates):
    B = Bootstrap_method(coverages[:,i])
    conf = B.conf_interval(95)
    print rate,2**rate, B.mean, conf[0], conf[1]

# make histogram of coverages distributions
hist = []
for i in range(len(rates)):
    a = Histogram(coverages[:,i],resolution=50,range_=[0,1])
    a.normalise()
    hist += [a.hist[:,1]]
with open('hist.dat','w') as f:
    for i,subhist in enumerate(np.transpose(hist)):
        f.write(str(a.hist[i,0])+'\t')
        for j in subhist:
            f.write(str(j)+'\t')
        f.write('\n')

