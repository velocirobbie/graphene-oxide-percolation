import numpy as np

class Histogram(object):
    def __init__(self,data,outfilename='hist.dat',
            resolution=0,range_=0):
        self.data = np.array(data)
        self.out = outfilename
        self.resolution = resolution
        
        #print 'Initialising histograpm ',self.out
        if not self.resolution: 
            self.resolution = int(np.amax(self.data.shape)/500)
            if self.resolution == 0:
                raise ValueError('Set your own resolution, not enough points')
        #print 'resolution = ',self.resolution
        if self.data.ndim == 1:
            if range_:
                self.low = range_[0]
                self.high = range_[1]
            else:    
                self.low = np.amin(self.data)
                self.high = np.amax(self.data)
            #print 'range = ',self.low,self.high
            self.hist = self.twodplot()
        
        if self.data.ndim == 2:
            #if range_ != 0:
            #    self.xlow,self.xhigh = range_[:][0]
            #    self.ylow,self.yhigh = range_[:][1]
            #else:
            #    self.xlow = np.amin(self.data[:,0])
            #    self.xhigh = np.amax(self.data[:,0])
            #    self.ylow = np.amin(self.data[:,1])
            #    self.yhigh = np.amax(self.data[:,1])
            self.xlow = -1
            self.xhigh = 1
            self.ylow = -1
            self.yhigh = 1
            self.resolution = 30
            print 'range: ', self.xlow,self.xhigh,self.ylow,self.yhigh
            self.hist,self.xbin_size,self.ybin_size = self.threedplot()

    def normalise(self):
        normalisation_factor = sum(self.hist[:,1]) * self.bin_size
        #print 'nf = ',normalisation_factor
        self.hist[:,1] = self.hist[:,1] / normalisation_factor

    def twodplot(self):
        hist = np.zeros((self.resolution,2))
        bin_size = (self.high - self.low)/float(self.resolution)
        self.bin_size = bin_size
        #print 'bin_size = ',bin_size
        for i in range(self.resolution):
            hist[i,0] = self.low + (bin_size * (i + 0.5))
        
        shifted_data = self.data - self.low
        for point in shifted_data:
            bin_ = int(round((point - (0.5 * bin_size))/bin_size))
            if point == 0:
                bin_ = 0
            if point == self.high - self.low:
                bin_ = self.resolution -1 
            #print point, bin_, (point - (0.5 * bin_size))/bin_size
            hist[bin_,1] += 1
        return hist

    def write_2d(self, data, out):
        with open(out,'w') as f:
            for point in data:
                f.write(str(point[0])+' \t'+str(point[1])+'\n')
        print 'Written 2D histogram to ',out

    def threedplot(self):
        hist = np.zeros((self.resolution,self.resolution))
        xbin_size = (float(self.xhigh) - self.xlow)/self.resolution
        ybin_size = (float(self.yhigh) - self.ylow)/self.resolution
        print 'bins: ', xbin_size, ybin_size
        shifted_xdata = self.data[:,0] - self.xlow
        shifted_ydata = self.data[:,1] - self.ylow
        for i in range(len(shifted_xdata)):
            x = round((shifted_xdata[i] - (0.50001 *xbin_size))/xbin_size)
            y = round((shifted_ydata[i] - (0.50001 *ybin_size))/ybin_size)
            #print x,y, shifted_xdata[i], shifted_ydata[i]
            hist[x,y] += 1
        return hist,xbin_size,ybin_size

    def write_3d(self,data,out):
        with open(out,'w') as out:
            for x in range(self.resolution):
                for y in range(self.resolution):
                    xbin = self.xlow + (self.xbin_size * (x + 0.5))
                    ybin = self.ylow + (self.ybin_size * (y + 0.5))
                    out.write(str(xbin)+' \t'+str(ybin)+' \t'+
                            str(data[x][y])+' \n')
                out.write('\n')
        print 'Written 3D histogram to ',self.out

    def write(self, data=[], out=''):
        if not len(data): data = self.hist
        if not out: out = self.out
        if self.data.ndim == 1:
            self.write_2d(data, out)
        else:
            self.write_3d(data, out)
