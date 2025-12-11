"File to rename cross sections so that they are machine readable"

import os
import sys

# function to renamte files
def rename(fName):

    # check if file has .endf in it
    if not ".endf" in fName:
        print(f"Skipped renaming {fName}")
        return fName

    # remove n- and .endf ending
    fName = fName[2:-5]

    # check for metaStable states
    metaStable = False
    if "m1" in fName:
        metaStable = True
        fName = fName[:-2]

    # remove middle nuclide portion
    if len(fName) == 9: # one letter name e.g. "U"
        fName = fName[:3] + fName[6:]
    if len(fName) == 10: # two letter name e.g. "Th"
        fName = fName[:3] + fName[7:]

    if metaStable:
        fName += "0001"
    if not metaStable:
        fName += "0000"
    
    return fName

# get list of files
fNames = os.listdir("../rawData/ENDF-B-VIII.0/neutrons")
path = "../rawData/ENDF-B-VIII.0/neutrons"

# loop over file names and rename each one
for fName in fNames:
    #print(f"OLD:{fName}  NEW:{rename(fName)}")
    fOld = os.path.join(path,fName)
    fNew = os.path.join(path,rename(fName))
    #print(f"{fOld} : {fNew}")
    os.rename(fOld,fNew)
