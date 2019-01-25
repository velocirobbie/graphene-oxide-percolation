import numpy as np

class Bootstrap_method(object):
    def __init__(self, xdata, resample_size=False, resamples=10000):
        
        sample_size = len(xdata)
        if resample_size is False:
            resample_size = sample_size
        self.resamples = resamples
         
        self.mean = self.arithmetic_mean(xdata)
        
        means = []
        for i in range(resamples):
            resample = self.resample(xdata, resample_size) 
            means += [ self.arithmetic_mean(resample) ]
        self.means = np.sort( np.array(means) )

    def conf_interval(self, interval):
        index = int(round( self.resamples * (100 - interval) / 100.0 ))
        lower = self.means[index - 1]
        upper = self.means[self.resamples - index]
        return [lower,upper]

    def arithmetic_mean(self,sample):
        return float(sum(sample))/len(sample)

    def resample(self, x, N):
        index = np.random.randint(len(x), size=N)
        return x[index]

