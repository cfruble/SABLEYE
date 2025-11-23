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
        # mt = 18
        # this could be a variable or a defailt
        fissionable = ['0922350000','0922380000']
        for isotope in self.trackedIsotopes:
            # loop through all isotopes
            # check if fissionable
            if isotope in fissionable:
                # get cross section
                # load in fission products data
                # loop over each isotope in FP data and add to Bateman Matrix
                pass

    def addTransmutations(self):
        tranmutationRxns = [
                {"i": 1, "MT": 4, "Reaction": "(n,n)", "A": "A", "Z": "Z", "M": "M+1"},
                {"i": 2, "MT": 16, "Reaction": "(n,2n)", "A": "A-1", "Z": "Z", "M": "M-1"},
                {"i": 3, "MT": 17, "Reaction": "(n,3n)", "A": "A-2", "Z": "Z", "M": None},
                #{"i": 4, "MT": 18, "Reaction": "(n,f)", "A": "FP", "Z": None, "M": None},
                {"i": 5, "MT": 22, "Reaction": "(n,na)", "A": "A-4", "Z": "Z-2", "M": None},
                {"i": 6, "MT": 23, "Reaction": "(n,n3a)", "A": "A-12", "Z": "Z-6", "M": None},
                {"i": 7, "MT": 24, "Reaction": "(n,2na)", "A": "A-5", "Z": "Z-2", "M": None},
                {"i": 8, "MT": 25, "Reaction": "(n,3na)", "A": "A-6", "Z": "Z-2", "M": None},
                {"i": 9, "MT": 28, "Reaction": "(n,np)", "A": "A-1", "Z": "Z-1", "M": None},
                {"i": 10, "MT": 29, "Reaction": "(n,n2a)", "A": "A-8", "Z": "Z-2", "M": None},
                {"i": 11, "MT": 32, "Reaction": "(n,nd)", "A": "A-2", "Z": "Z-1", "M": None},
                {"i": 12, "MT": 33, "Reaction": "(n,nt)", "A": "A-3", "Z": "Z-2", "M": None},
                {"i": 13, "MT": 34, "Reaction": "(n,nhe3)", "A": "A-3", "Z": "Z-2", "M": None},
                {"i": 14, "MT": 37, "Reaction": "(n,4n)", "A": "A-3", "Z": "Z-2", "M": None},
                {"i": 15, "MT": 41, "Reaction": "(n,2np)", "A": "A-2", "Z": "Z-1", "M": None},
                {"i": 16, "MT": 44, "Reaction": "(n,n2p)", "A": "A-2", "Z": "Z-1", "M": None},
                {"i": 17, "MT": 45, "Reaction": "(n,npa)", "A": "A-5", "Z": "Z-2", "M": None},
                {"i": 18, "MT": 102, "Reaction": "(n,g)", "A": "A+1", "Z": "Z", "M": "M+1"},
                {"i": 19, "MT": 103, "Reaction": "(n,p)", "A": "A-1", "Z": "Z-1", "M": None},
                {"i": 20, "MT": 104, "Reaction": "(n,d)", "A": "A-1", "Z": "Z-1", "M": None},
                {"i": 21, "MT": 105, "Reaction": "(n,t)", "A": "A-2", "Z": "Z-1", "M": None},
                {"i": 22, "MT": 106, "Reaction": "(n,he3)", "A": "A-2", "Z": "Z-2", "M": None},
                {"i": 23, "MT": 107, "Reaction": "(n,a)", "A": "A-3", "Z": "Z-2", "M": None},
                {"i": 24, "MT": 108, "Reaction": "(n,2a)", "A": "A-7", "Z": "Z-4", "M": None},
                {"i": 25, "MT": 111, "Reaction": "(n,2p)", "A": "A-1", "Z": "Z-2", "M": None},
                {"i": 26, "MT": 112, "Reaction": "(n,pa)", "A": "A-4", "Z": "Z-3", "M": None},
                {"i": 27, "MT": 113, "Reaction": "(n,2a)", "A": "A-7", "Z": "Z-4", "M": None},
                {"i": 28, "MT": 115, "Reaction": "(n,pd)", "A": "A-2", "Z": "Z-2", "M": None},
                {"i": 29, "MT": 116, "Reaction": "(n,pt)", "A": "A-3", "Z": "Z-2", "M": None},
                {"i": 30, "MT": 117, "Reaction": "(n,da)", "A": "A-5", "Z": "Z-3", "M": None},
                ]
        for targetIndex, targetIso in enumerate(self.trackedIsotopes):
        # loop through isotopes in self.trackedIsotopes
            for productIndex, productIso in enumerate(self.trackedIsotopes):
            # run second loop through tracked isotopes

            # skip for case when the same
                if targetIndex == productIndex: continue

                # get difference between isotopes A and Z
                # if isotopes difference match pattern in data above, then get cross section using MT number
                # find reaction rate using flux and add to bateman matrix
                self.BM[targetIndex][productIndex] += 0



    
    def exportBatemanMatrix(self):
        """Exports data from Bateman matrix that can then be used by simulation model"""
        return self.BM


# testing
if __name__ == '__main__':
    tI = ['0922380000','0902340000','0912340000']
    BM = batemanMatrix(tI)
    BM.addDecay(".")
    print(BM.exportBatemanMatrix())
    


