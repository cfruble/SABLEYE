"Script to create Bateman matrix"

import numpy as np
import json
from typing import List, Union
import os

class testing:
    def __init__(self):
        pass
    def method(self):
        print("method")
    
class batemanMatrix:
    """
    Creates Bateman matrix using preprocessed data
    """
    def __init__(self,trackedIsotopes: List[Union[str,int]]=None):
        if trackedIsotopes == None:
            raise ValueError("Nuclide List cannot be blank")
        for isotope in trackedIsotopes: # check if isotopes are valid
            try:
                pass
                #nucname.id(isotope)
            except:
                print(f"Isotope name not valid for {isotope}")
        
        # Add isotope data to system
        self.trackedIsotopes = trackedIsotopes
        
        # create empty matrix to hold coefficients
        N = len(trackedIsotopes)
        self.BM = np.zeros([N,N]) # fully dense matrix

    def addDecay(self,fPath):
        with open(os.path.join(fPath,"decayData.json")) as file:
            try:
                decayData = json.load(file)
            except FileNotFoundError:
                print(f"Error : decayData.json file could not be found at {fPath}")
        # loop through tracked isotopes
        for parentIndex, parent in enumerate(self.trackedIsotopes):
            try:
                decayConst = decayData[parent]['decayConst']
                childNames = decayData[parent]['childNames']
                childProbs = decayData[parent]['childProbs']
            except KeyError:
                print(f"Error : key {parent} not found in decayData")
            
            # add decayConstants into diagonals on BM
            self.BM[parentIndex][parentIndex] -= decayConst
            
            # add decayCoefficents to off diagonals
            for childName, childProb in zip(childNames,childProbs): # loop over decay products
                # check if child is a tracked isotope
                try:
                    childIndex = self.trackedIsotopes.index(childName)
                    # add data into matrix
                    self.BM[childIndex][parentIndex] += decayConst * childProb
                except ValueError:
                    print(f"Error : Decay product {childName} from {parent} not in trackedIsotopes")

    def addFissionYields(self):
        pass

    def addTransmutations(self):
        pass
    
    def exportBatemanMatrix(self):
        """Exports data from Bateman matrix that can then be used by simulation model"""
        return self.BM


# testing
if __name__ == '__main__':
    tI = ['0922380000','0902340000','0912340000']
    BM = batemanMatrix(tI)
    BM.addDecay(".")
    print(BM.exportBatemanMatrix())
    


