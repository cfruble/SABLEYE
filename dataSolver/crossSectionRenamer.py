"""
File to rename cross section files into a canonical, machine-readable format.

This script processes ENDF cross section files in './rawData/ENDF-B-VIII.0/neutrons',
renaming them to standardized isotope codes suitable for programmatic use.

Usage
-----
Run this script after extracting ENDF data to the 'neutrons' folder.
All files with '.endf' extensions are converted to canonical codes.

Functions
---------
rename(fName)
    Converts ENDF cross section filename to isotope code.
"""

import os
import sys

# function to renamte files
def rename(fName):
    """
    Convert ENDF cross section filename to canonical isotope code.

    Removes "n-" prefix and ".endf" suffix, 
    processes meta-stable state information, and
    simplifies isotope naming for machine readability.

    Parameters
    ----------
    fName : str
        Original filename (e.g., "n-092_U_235.endf").

    Returns
    -------
    str
        Renamed string in canonical format (e.g., '0922350000' or '0922350001').
    """
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
fNames = os.listdir("./rawData/ENDF-B-VIII.0/neutrons")
path = "./rawData/ENDF-B-VIII.0/neutrons"

# loop over file names and rename each one
for fName in fNames:
    #print(f"OLD:{fName}  NEW:{rename(fName)}")
    fOld = os.path.join(path,fName)
    fNew = os.path.join(path,rename(fName))
    #print(f"{fOld} : {fNew}")
    os.rename(fOld,fNew)
