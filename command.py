from sim import Sim
import numpy as np
#a = Sim(4,20)
import sys

dr = 0.001
rate = 10
np.random.seed(1)

a = Sim(rate, dr, Nmonte_points=10000,graph=True, error=True)
a.simulate()
a.print_output()

