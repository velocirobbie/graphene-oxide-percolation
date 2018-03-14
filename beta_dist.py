#from scipy.stats import beta
from scipy.optimize import curve_fit
from scipy.special import gamma


def beta(x, a, b):
    bottom = gamma(a)*gamma(b) / gamma(a+b)
    top = x**(a-1) * (1-x)**(b-1)
    return top / bottom

x = []
y = []
with open('radii16.hist','r') as f:
    for line in f:
        line = line.split()
        x += [ float(line[0]) ]
        y += [ float(line[1]) ]

param, conv = curve_fit(beta, x, y)

for i in range(100):
    print i/100.0, beta(i/100.0,*param)
