"File to measure preofmance on decay"

import sys
import os
import matplotlib.pyplot as pyplot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time as tme

sys.path.append(os.path.join(os.path.dirname(__file__), '../dataSolver'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from batemanMatrix import batemanMatrix
from solver import fuelSystem, reactor
from plotter import plotLinegraph

Nruns = 100

# Function to show sparse matrix
# this function was partially written by generative AI

def visualize_sparse_matrix(matrix,fName):
    
    # Create a figure and axis for plotting
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # plot out matrix
    ax.spy(matrix,aspect="equal")
    
    # Set labels and title
    #ax.set_title("Sparse Matrix Visualization")
    ax.set_xlabel("childIsotope")
    ax.set_ylabel("parrentIsotope")
    
    # save output for later comparison
    fig.savefig(fName,dpi=600)

# array of isotopes to be tracked for 4 isotope case
isotopes4 = ['0922380000','0902340000','0912340000','0922340000']

# array of isotopes to be tracked for 11 isotopes case (Thorium decay chain)
isotopes11 = ['0902320000','0882280000','0892280000','0902280000',
              '0882240000','0862200000','0842160000','0822120000',
              '0832120000','0842120000','0812080000']

isotopes18 = ['0922350000','0922360000','0922370000','0922380000','0922390000','0922400000',
            '0932350000','0932360000','0932370000','0932380000','0932390000','0932400000',
            '0942390000','0942400000','0942410000','0942420000','0942430000','0942440000']

# create Bateman Matrix
BM4 = batemanMatrix(isotopes4)
BM4.addDecay("../procData")
Q4 = BM4.exportBatemanMatrix()
BM11 = batemanMatrix(isotopes11)
BM11.addDecay("../procData")
Q11 = BM11.exportBatemanMatrix()
BM18 = batemanMatrix(isotopes18)
BM18.addDecay("../procData")
BM18.addTransmutations({"values":np.array([1])})
Q18 = BM18.exportBatemanMatrix()


visualize_sparse_matrix(Q4,"normalQ4.png")
visualize_sparse_matrix(Q11,"normalQ11.png")
visualize_sparse_matrix(Q18,"normalQ15.png")

# create timesteps
times = np.logspace(0,18.1,num=200)

# load Bateman matrix into reactor object
r4 = reactor(Q4)
r11 = reactor(Q11)
r18 = reactor(Q18)

startT = tme.perf_counter()
i = 0
while i < Nruns:
    fs4 = fuelSystem(isotopes4,np.array([1,0,0,0]))
    for time in times:
        # simulate reactor and update
        r4.timeSimulate(fs4,time)
    i += 1
endT = tme.perf_counter()
elapsedTime = endT-startT
print(f"4 isotope system runtime : {elapsedTime/Nruns}")

startT = tme.perf_counter()
i = 0
while i < Nruns:
    fs11 = fuelSystem(isotopes11,np.array([1,0,0,0,0,0,0,0,0,0,0]))
    for time in times:
        # simulate reactor and update
        r11.timeSimulate(fs11,time)
    i += 1
elapsedTime = tme.perf_counter() - startT
print(f"11 isotope system runtime : {elapsedTime/Nruns}")

startT = tme.perf_counter()
i = 0
while i < Nruns:
    fs18 = fuelSystem(isotopes18,np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    for time in times:
        # simulate reactor and update
        r18.timeSimulate(fs18,time)
    i += 1
elapsedTime = tme.perf_counter() - startT
print(f"18 isotope system runtime : {elapsedTime/Nruns}")