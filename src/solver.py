"""
Main solver implementation for SABLEYE.

Provides classes and methods to manipulate the fuel system, run reactor
simulations via the Bateman matrix, and perform reprocessing operations.
"""

import numpy as np
from scipy.linalg import expm

class fuelSystem():
    """
    Fuel system holding information on isotopic history.

    Stores isotope names, concentrations, and keeps a history of fuel compositions
    through simulation steps.
    """
    
    def __init__(self,isotopes,concentrations):
        """
        Initialize fuel system with initial isotopes and concentrations.

        Parameters
        ----------
        isotopes : list of str
            List of isotope names.
        concentrations : array-like
            List or array of starting concentrations (ordered to match isotopes).

        Raises
        ------
        ValueError
            If the isotopes and concentrations are not of the same length.
        """
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
    
    def appendHistory(self,conentrations):
        """
        Add a new state to the system's history.

        Parameters
        ----------
        concentrations : array-like
            Isotope concentrations to append (must match isotope count).

        Raises
        ------
        ValueError
            If the input concentrations have wrong length.
        """
        
        # check that new states are correct length
        if self.dataLength != len(conentrations):
            raise ValueError("Invalid concentration length added")
        
        # update system present state and append new data
        self.con = conentrations
        self.history = np.append(self.history, conentrations, axis=0)
    
    def exportHistory(self,fName=None):
        """
        Export isotope history as a NumPy array or .npy file.

        Parameters
        ----------
        fName : str, optional
            If given, saves history to a NumPy binary file. If None, returns the array.

        Returns
        -------
        np.ndarray or None
            Isotope history array if fName is not provided; else None.
        """
        if fName == None:
            return self.history.reshape(-1,len(self.iso))
        np.save(fName,self.history)

    
class reactor():
    """
    Reactor class for simulation analysis.

    Encapsulates Bateman matrix application to the fuel system for time evolution.
    """
    
    def __init__(self,batemanMatrix):
        """
        Initialize reactor with Bateman matrix.

        Parameters
        ----------
        batemanMatrix : np.ndarray
            Matrix for solving Bateman equations (transmutation and decay rates).
        """
        self.BM = batemanMatrix
        
    
    def timeSimulate(self,fuelSys,time):
        """
        Method to apply bateman matrix to system for specified time and appends fuelSystem object"

        Parameters
        ----------
        fuelSys : fuelSystem
            Fuel system to evolve.
        time : float
            Simulation time interval.

        Raises
        ------
        ValueError
            If fuelSys is not a fuelSystem object.
        """
        # check that passed fuelSys is an instance of the fuelSystem
        if not isinstance(fuelSys,fuelSystem):
            raise ValueError('Input to timeSimulate is not a fuelSystem object!')
        
        # use matrix exponentiation to solve system
        N_new = expm(self.BM * time) @ fuelSys.con
        #print(f"{self.BM * time}")
        #print(f"{fuelSys.con}")
        #print(f"{N_new}")
        
        # update system with new information
        fuelSys.appendHistory(N_new)
        
class reprocess():
    """
    Reprocessing class for simulation analysis.

    Applies reprocessing schemes to isotope vectors, with options for normalization.
    """
    
    def __init__(self,add,mult,reNorm=False):
        """
        Initialize reprocessing scheme.

        Parameters
        ----------
        add : array-like
            Vector detailing isotopes added to system.
        mult : array-like
            Vector detailing fractions that are removed/modified by reprocessing.
        reNorm : bool, optional
            If True, isotope vector is renormalized after reprocessing.
        """
        self.add = add
        self.mult = mult
        self.reNorm = reNorm

    def repo(self,fuelSys):
        """
        Apply the reprocessing scheme to a fuelSystem object and append to history.

        Parameters
        ----------
        fuelSys : fuelSystem
            Fuel system to modify with reprocessing.

        Raises
        ------
        ValueError
            If fuelSys is not a fuelSystem object.
        """
        
        # check that passed fuelSys is an instance of the fuelSystem
        if not isinstance(fuelSys,fuelSystem):
            raise ValueError('Input to repo is not a fuelSystem object!')
        
        N_new = self.add + np.dot(self.mult,fuelSys.con)
        if self.reNorm:
            # Normalize isotope concentrations so that they add to 1
            N_new /= sum(N_new)
        
        # append data after reprocessing to fuelSystem object
        fuelSys.appendHistory(N_new)
        
