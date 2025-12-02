"Implementation for main solver of SABLEYE"

import numpy as np
from scipy.linalg import expm

class fuelSystem():
    "Fuel system which contains information on isotopic history of system"
    
    def __init__(self,isotopes,concentrations):
        "Initialize fuel system with initial isotopes and concentrations"
        # check that isotope list and conetration list are same length
        if len(isotopes) != len(concentrations):
            raise ValueError('Isotope and concentration list not equal')
        
        # store data length for future checking
        self.dataLength = len(isotopes)
        
        # store data into object
        self.iso = isotopes
        self.con = concentrations

        # save initial data into history
        self.history = concentrations
    
    def appendHistroy(self,conentrations):
        "Method to add new state to system history"
        
        # check that new states are correct length
        if self.dataLength != len(conentrations):
            raise ValueError("Invalid concentration length added")
        
        # update system present state and append new data
        self.con = conentrations
        self.history = np.append(self.history, conentrations, axis=0)
    
    def exportHistory(self,fName):
        "Exports histroy to fName.npy for use in plotting or safekepping"
        np.save(fName,self.history)

    
class reactor():
    "Implements reactor class for analysis"
    
    def __init__(self,batemanMatrix):
        self.BM = batemanMatrix
        
    
    def timeSimulate(self,fuelSys,time):
        "Method to apply bateman matrix to system for specified time and appends fuelSystem object"
        
        # check that passed fuelSys is an instance of the fuelSystem
        if not isinstance(fuelSys,fuelSystem):
            raise ValueError('Input to timeSimulate is not a fuelSystem object!')
        
        # use matrix exponentiation to solve system
        N_new = fuelSys.con @ expm(self.BM * time)
        
        # update system with new information
        fuelSys.appendHistroy(N_new)
        
class reprocess():
    "Implements reprocessing class for analysis"
    
    def __init__(self,add,mult,reNorm=False):
        """
        Docstring for __init__
        
        :param add: Isotope vector detailing what should be added to system
        :param mult: Isotope vector detailing what fractions are removed
        :param reNorm: Isotope vector specifying if system should be renormalized
        """
        self.add = add
        self.mult = mult
        self.reNorm = reNorm

    def repo(self,fuelSys):
        "Method to apply reprocessing scheme to fuelSystem object and append history"
        
        # check that passed fuelSys is an instance of the fuelSystem
        if not isinstance(fuelSys,fuelSystem):
            raise ValueError('Input to repo is not a fuelSystem object!')
        
        N_new = self.add + np.dot(self.mult,fuelSys.con)
        if self.reNorm:
            # Normalize isotope concentrations so that they add to 1
            N_new /= sum(N_new)
        
        # append data after reprocessing to fuelSystem object
        fuelSys.appendHistroy(N_new)
        
