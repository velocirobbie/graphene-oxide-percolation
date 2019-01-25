from sim import Sim
import numpy as np

dr = 0.001
rate = 10

a = Sim(rate, dr, graph=True, error=True)
a.simulate()
a.print_output()

