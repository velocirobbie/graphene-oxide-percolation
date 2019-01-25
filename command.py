from sim import Sim
import numpy as np
#a = Sim(4,20)
import sys

dr = 0.001
rate = 10

a = Sim(rate, dr, graph=True, error=True)
a.simulate()
a.print_output()

