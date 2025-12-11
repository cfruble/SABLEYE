"File to test decay data in batemanMatrix.py"

import sys
import os
import matplotlib.pyplot as pyplot
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../dataSolver'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from batemanMatrix import batemanMatrix
from solver import fuelSystem, reactor
from plotter import plotLinegraph

# array of isotopes to be tracked
isotopes = ['0922380000','0902340000','0912340000','0922340000']

# create Bateman Matrix
BM = batemanMatrix(isotopes)
BM.addDecay("../procData")
Q = BM.exportBatemanMatrix()

# create fuelsystem
fs = fuelSystem(isotopes,np.array([1,0,0,0]))

# create timesteps
times = np.logspace(0,18.1,num=200)

# load Bateman matrix into reactor object
r = reactor(Q)

for time in times:
    # simulate reactor and update
    r.timeSimulate(fs,time)

# store results
results = fs.exportHistory()

plotLinegraph(times,results,isotopes,"test_decay_linegraph.png")
