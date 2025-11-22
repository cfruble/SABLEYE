import numpy as np
import csv
from typing import List, Union

class decayChain:
    """
    Solves for decay chains and decay related things
    """
    def __init__(self,fPath):
        "Pass filePath to decayData.csv; converts this to dictionary"

class BuildBateman:
    """
    Creates Bateman matrix
    """
    def __init__(self,trackedIsotopes: List[Union[str,int]]=None):
        if trackedIsotopes == None:
            raise ValueError("Nuclide List cannot be blank")
        for isotope in trackedIsotopes: # check if isotopes are valid
            try:
                nucname.id(isotope)
            except:
                print(f"Isotope name not valid for {}")
        

    def addDecay(self):
        pass

    def addFissionYields(self):
        pass

    def addTransmutations(self):
        pass