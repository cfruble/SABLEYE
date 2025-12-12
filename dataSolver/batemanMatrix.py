"""
Script to create and manipulate Bateman transmutation/decay matrix for isotope evolution modeling.

This module builds the Bateman matrix using preprocessed decay, fission, and transmutation data
and supports exporting and saving the matrix for later use in simulation workflows.

Usage
-----
- Initialize with a list of tracked isotopes (canonical isotope strings).
- Use `addDecay`, `addTransmutations`, etc., to build the matrix.
- Export or save the resulting matrix for use elsewhere.
"""

import numpy as np
import json
from typing import List, Union
import os
import cross_section_homogenizer as csh

class batemanMatrix:
    """
    Builds a Bateman matrix using preprocessed nuclear data for decay,
    fission yields, and transmutation reactions.

    The resulting matrix models time evolution of a system of tracked isotopes.
    """
    def __init__(self,trackedIsotopes: List[Union[str,int]]=None):
        """
        Initialize Bateman matrix for a set of tracked isotopes.

        Parameters
        ----------
        trackedIsotopes : list of str or int
            List of canonical isotope identifiers to track.

        Raises
        ------
        ValueError
            If the nuclide list is empty or None.
        """
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
        """
        Add isotope decay information to the matrix from a JSON file.

        The decay data should contain decay constants and branching probabilities
        for each parent isotope to possible child isotopes.

        Parameters
        ----------
        fPath : str
            Path to directory where 'decayData.json' can be found.

        Raises
        ------
        FileNotFoundError
            If the decay JSON file is not found.
        KeyError
            If a tracked isotope is missing required decay keys in the JSON.
        """
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
        """
        Placeholder for adding fission yield data to the Bateman matrix.

        Intended to supplement the matrix for fissionable nuclides based on
        cross sections and yield files.

        Returns
        -------
        None
        """
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

    @staticmethod
    def isotopeChange(isoName: str, deltaA:int, deltaZ:int, deltaM = None):
        """
        Update isotopes names with change in A, Z, M AAAZZZMMMM.

        Parameters
        ----------
        isoName : str
            Isotope code in format AAAZZZMMMM.
        deltaA : int
            Change in mass number (A).
        deltaZ : int
            Change in atomic number (Z).
        deltaM : str or None, optional
            Change in metastable state ("+1", "-1", or None).

        Returns
        -------
        str
            New isotope code reflecting the changes.
        """
        
        A = int(isoName[0:3]) + deltaA
        Z = int(isoName[3:7]) + deltaZ
        M = isoName[7:10]
        if deltaM == None:
            pass # do nothing, no updates
            if deltaM == "+1": # go to excited state
                if M == "0001":
                    M = "0010"
                if M == "0000":
                    M = "0001"
            if deltaM == "-1":
                if M == "0010":
                    M = "0001"
                if M == "0001":
                    M = "0000"
        # re assemble A and Z
        return f"{A:03d}"+f"{Z:03d}"+M


    def addTransmutations(self,energy_spectrum: dict[str, np.ndarray]):
        """
        Add transmutation reaction data (non-decay, non-fission reactions)
        to the Bateman matrix using single-group cross sections.

        The reaction table is derived from literature and includes many 
        neutron-induced reactions; it relies on the CrossSectionHomogenizer.

        Parameters
        ----------
        energy_spectrum : dict[str, np.ndarray]
            Energy bins and weights used for spectrum-weighted cross sections.

        Returns
        -------
        None
        """
        
        # reaction table generated by ChatGPT from Table in M. Lovecky et. al.
        transmutationRxns = [
            {"i": 1, "MT": 4, "Reaction": "(n,n)", "A": 0, "Z": 0, "M": "+1"},
            {"i": 2, "MT": 16, "Reaction": "(n,2n)", "A": -1, "Z": 0, "M": "-1"},
            {"i": 3, "MT": 17, "Reaction": "(n,3n)", "A": -2, "Z": 0, "M": None},
            {"i": 4, "MT": 18, "Reaction": "(n,f)", "A": "FP", "Z": None, "M": None},
            {"i": 5, "MT": 22, "Reaction": "(n,na)", "A": -4, "Z": -2, "M": None},
            {"i": 6, "MT": 23, "Reaction": "(n,n3a)", "A": -12, "Z": -6, "M": None},
            {"i": 7, "MT": 24, "Reaction": "(n,2na)", "A": -5, "Z": -2, "M": None},
            {"i": 8, "MT": 25, "Reaction": "(n,3na)", "A": -6, "Z": -2, "M": None},
            {"i": 9, "MT": 28, "Reaction": "(n,np)", "A": -1, "Z": -1, "M": None},
            {"i": 10, "MT": 29, "Reaction": "(n,n2a)", "A": -8, "Z": -2, "M": None},
            {"i": 11, "MT": 32, "Reaction": "(n,nd)", "A": -2, "Z": -1, "M": None},
            {"i": 12, "MT": 33, "Reaction": "(n,nt)", "A": -3, "Z": -2, "M": None},
            {"i": 13, "MT": 34, "Reaction": "(n,nhe3)", "A": -3, "Z": -2, "M": None},
            {"i": 14, "MT": 37, "Reaction": "(n,4n)", "A": -3, "Z": 0, "M": None},
            {"i": 15, "MT": 41, "Reaction": "(n,2np)", "A": -2, "Z": -1, "M": None},
            {"i": 16, "MT": 44, "Reaction": "(n,n2p)", "A": -2, "Z": -1, "M": None},
            {"i": 17, "MT": 45, "Reaction": "(n,npa)", "A": -5, "Z": -2, "M": None},
            {"i": 18, "MT": 102, "Reaction": "(n,g)", "A": +1, "Z": 0, "M": "+1"},
            {"i": 19, "MT": 103, "Reaction": "(n,p)", "A": -1, "Z": -1, "M": None},
            {"i": 20, "MT": 104, "Reaction": "(n,d)", "A": -1, "Z": -1, "M": None},
            {"i": 21, "MT": 105, "Reaction": "(n,t)", "A": -2, "Z": -1, "M": None},
            {"i": 22, "MT": 106, "Reaction": "(n,he3)", "A": -2, "Z": -2, "M": None},
            {"i": 23, "MT": 107, "Reaction": "(n,a)", "A": -3, "Z": -2, "M": None},
            {"i": 24, "MT": 108, "Reaction": "(n,2a)", "A": -7, "Z": -4, "M": None},
            {"i": 25, "MT": 111, "Reaction": "(n,2p)", "A": -1, "Z": -2, "M": None},
            {"i": 26, "MT": 112, "Reaction": "(n,pa)", "A": -4, "Z": -3, "M": None},
            {"i": 27, "MT": 113, "Reaction": "(n,2a)", "A": -7, "Z": -4, "M": None},
            {"i": 28, "MT": 115, "Reaction": "(n,pd)", "A": -2, "Z": -2, "M": None},
            {"i": 29, "MT": 116, "Reaction": "(n,pt)", "A": -3, "Z": -2, "M": None},
            {"i": 30, "MT": 117, "Reaction": "(n,da)", "A": -5, "Z": -3, "M": None},
        ]

        # call data homogenizer and set to default values
        XSdata = csh.CrossSectionHomogenizer()

        for targetIndex, targetIso in enumerate(self.trackedIsotopes):
        # loop through isotopes in self.trackedIsotopes

            # loop through reactions and check if product is part of trackedIsotopes
            for rxnIndex, rxn in enumerate(transmutationRxns):
                prodIso = batemanMatrix.isotopeChange(targetIso,rxn['A'],rxn['Z'])
                print(rxnIndex)
                if prodIso in self.trackedIsotopes:
                    # add to bateman matrix
                    # get cross section and multiply by flux
                    iso_fPath = os.path.join('./rawData/ENDF-B-VIII.0/neutrons',targetIso)
                    print(iso_fPath)
                    XS = XSdata.get_one_group_xs(iso_fPath,targetIso,rxn["MT"])
                    totalFlux = 1000
                    self.BM += XS * totalFlux
                else:
                    print(f"ERROR : product isotope {prodIso} not in tracked isotopes for {rxn['Reaction']}")


    def exportBatemanMatrix(self):
        """
        Exports data from Bateman matrix that can then be used by simulation model.

        Returns
        -------
        np.ndarray
            The matrix representing all decay, fission, and transmutation coefficients.
        """
        
        return self.BM

    def saveBatemanMatrix(self,fName):
        """
        Save the Bateman matrix to a binary .npy file.

        Parameters
        ----------
        fName : str
            File name/path for the saved matrix.

        Returns
        -------
        None
        """
        np.save(fName,self.BM)


    


