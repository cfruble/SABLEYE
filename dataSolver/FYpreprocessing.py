"Helper module to process fission yield data into readable format from endf files using OpenMC"

"""
USAGE:
ENDF FY files should be placed in a folder "./rawFY"

"""

import openmc
from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt
import re
import os

def fNameRenamer(fName):
    # remove first part and file extension
    fName = fName[5:-5]
    metaStable = False
    # catch error for metastable states
    if "m1" in fName:
        metaStable = True
        # remove metastable ending
        fName = fName[:-2]
        
        

    # strip out isotope name
    fName = fName[:2] + fName[-3:]

    if metaStable:
        fName += "1000"
    else:
        fName += "0000"

    return fName

# FY data threshold of significance
threshold = 1e-10

# get listing of fission yield files
fNames = os.listdir("./rawFY")

for fName in fNames: #iterate through each file path
    fPath = os.path.join("./rawFY",fName)
    #print(fPath)
    data = openmc.data.FissionProductYields(fPath)

    isotopeList = []
    yieldList = []

    for key in data.independent[0]:
        # check if value above certain threshold
        value = data.independent[0][key].nominal_value
        if value > threshold:
            #yieldList.append(data.independent[0][key].nominal_value)
            #print(key)

            #fix formating for metastable elements
            if "_m1" in key:
                key = key[:-3]
                key += 'M'

            if "_m2" in key:
                key = key[:-3]
                key += 'M'

            yieldList.append(value)
            isotopeList.append(key)
        

    # create filenames that are readable by endf
    #print(fNameRenamer(fName))

    lines = []
    for i in range(len(yieldList)):
        line = f"{isotopeList[i]} , {yieldList[i]} \n"
        lines.append(line)
    
    with open(f"./processedFY/{fNameRenamer(fName)}",'w') as f:
        f.writelines(lines)

        