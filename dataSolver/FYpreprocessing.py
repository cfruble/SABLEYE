"""
Helper module to process fission yield (FY) data from ENDF files using OpenMC.

This script reads ENDF FY files (usually placed in `./rawData/ENDF-B-VIII.0/nfy`),
extracts isotopes and their independent yields above a set threshold, and writes
the results in a concise comma-separated format suitable for further processing.

Usage
-----
Make sure your ENDF FY files are located in `./rawData/ENDF-B-VIII.0/nfy/`.
Output files are written to `./procData/FY/`, named using the processed isotope code.

Functions
---------
fNameRenamer(fName)
    Converts ENDF file names to a canonical isotope code used in output files.

isoRenamer(isoName)
    Placeholder for renaming isotope strings to canonical format (not yet implemented).
"""

import openmc
from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt
import re
import os



def fNameRenamer(fName):
    """
    Convert ENDF FY filename to canonical isotope code for output.

    Strips prefixes/suffixes, adjusts for meta-stable states, and 
    produces a unique code used in output file naming.

    Parameters
    ----------
    fName : str
        Original filename from ENDF FY directory.

    Returns
    -------
    str
        Canonical isotope code, e.g. "0060140000" or meta-stable variant.
    """
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

def isoRenamer(isoName):
    """
    Placeholder function for renaming isotope strings (not yet implemented).

    Parameters
    ----------
    isoName : str
        Isotope name.

    Returns
    -------
    None
    """
    pass

# FY data threshold of significance
threshold = 1e-10

# get listing of fission yield files
fNames = os.listdir("./rawData/ENDF-B-VIII.0/nfy")

for fName in fNames: #iterate through each file path
    # remove non-endf files from consideration
    if not ".endf" in fName:
        print(fName)
        continue
    
    fPath = os.path.join("./rawData/ENDF-B-VIII.0/nfy",fName)
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
        

    # rewrite isotope names in list from C14 -> 0060140000
    

    lines = []
    for i in range(len(yieldList)):
        line = f"{isotopeList[i]} , {yieldList[i]} \n"
        lines.append(line)
    
    with open(f"./procData/FY/{fNameRenamer(fName)}",'w') as f:
        f.writelines(lines)

        
