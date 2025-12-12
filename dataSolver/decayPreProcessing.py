"""
Script to process ENDF decay data into usable format.

This module reads ENDF decay data files, extracts half-lives, decay modes, and probabilities,
and creates a JSON dictionary suitable for simulation models. It provides tools to parse file
names, convert time units, and derive child isotopes according to decay chains.

Usage
-----
Place ENDF decay files in './rawData/ENDF-B-VIII.0/decay/'
Run the main script to generate './procData/decayData.json'.

Classes
-------
decayProcessing
    Parse and process ENDF decay data files into a dictionary.

decayChain
    Loads decay dictionary and (partially) supports decay chain queries.

Functions
---------
generateDecayData
    (Stub) Placeholder for future encapsulated decay data generator.
"""


import os
import re
import json
from typing import List, Union

# potential functional encapsulation
def generateDecayData(decayENDF_fPath: str, out_fName = "decayData.csv", out_fPath = "./", consoleLog = False):
    pass

class decayProcessing:
    """
    Extracts decay data from ENDF files and organizes it into a dictionary.

    Collects parent isotope, half-life (converted to seconds), decay modes,
    and probabilities for downstream simulation or analysis.
    """

    def __init__(self, decayENDF_fPath: str, consoleLog = False):
        """
        Initialize the decay data processor for ENDF decay files.

        Parameters
        ----------
        decayENDF_fPath : str
            Directory containing ENDF-formatted decay files (.endf).
        consoleLog : bool, optional
            If True, prints processing logs and summary.
        """
        self.consoleLog = consoleLog
        self.decayENDF_fPath = decayENDF_fPath
        self.fPaths = []
        self.fNames = []
        for fName in os.listdir(decayENDF_fPath):
            if fName.endswith('.endf'):
                self.fNames.append(fName)
        self.fNames.sort()

    @staticmethod
    def convert_to_seconds(time_string: str) -> float:
        """
        Convert various time unit strings to values in seconds.

        Parameters
        ----------
        time_string : str
            Half-life string such as '1.23 D', '10.5 S', '4.7 Y', etc.

        Returns
        -------
        float
            Equivalent seconds.

        Raises
        ------
        ValueError
            If time unit is not recognized.
        """
        time_string = time_string.replace(">","")
        time_string = time_string.replace("<","")

        # Conversion factors for different time units to seconds
        time_units_to_seconds = {
        'Y': 365 * 24 * 60 * 60,  # 1 year = 365 days = 24 hours/day = 60 minutes/hour = 60 seconds/minute
        'M': 60,   # 1 minute = 60 seconds
        'D': 24 * 60 * 60,        # 1 day = 24 hours/day = 60 minutes/hour = 60 seconds/minute
        'H': 60 * 60,             # 1 hour = 60 minutes * 60 seconds
        'S': 1,                   # 1 second = 1 second
        'MS': 1e-3,               # 1 millisecond = 1e-3 seconds
        'US': 1e-6,               # 1 microsecond = 1e-6 seconds
        'NS': 1e-9                # 1 nanosecond = 1e-9 seconds
        }

        # Split the string into two parts: value and unit
        parts = time_string.strip().split()

        # The first part is the significant value (can be a float or scientific notation)
        significant_value = float(parts[0])

        # The second part is the time unit
        time_unit = parts[1].upper()  # Ensure it's uppercase for consistency

        # Check if the time unit is in the dictionary
        if time_unit in time_units_to_seconds:
            # Convert the significant value to seconds
            seconds = significant_value * time_units_to_seconds[time_unit]
            return seconds
        else:
            raise ValueError(f"Unknown time unit: {time_unit}")      

    @staticmethod
    def convert_fName_to_AAAZZZMMMM(fName:str) -> str:
        """
        Convert ENDF decay filename to canonical isotope code (AAAZZZMMMM). Example: ENDF decay file name in format of 'dec-092_U_235.endf' into '0922350000'

        Parameters
        ----------
        fName : str
            File name like 'dec-092_U_235.endf'

        Returns
        -------
        str
            Canonical isotope code like '0922350000'
        """
        metastable = 0
        
        name = fName[4:-5] # remove 'dec-' and '.endf'
        if "m1" in name: # first metastable state
            name = name.replace("m1","") # remvoe m1
            metastable = 1
        elif "m2" in name: #second metastable state
            name = name.replace("m2","")
            metastable = 2
        name = re.sub(r'[^\d]', '', name) # remove nuclide name
        # add back metastable state information
        if metastable == 0:
            name += "0000"
        elif metastable == 1:
            name += "0001"
        elif metastable == 2:
            name += "0010"
        return name
        #return fName
    
    @staticmethod
    def childIsotopes(parent: str, decayModes: Union[List[str],None]) -> str:
        """
        Calculate child isotopes produced from various decay modes.

        Parameters
        ----------
        parent : str
            Canonical parent isotope code (AAAZZZMMMM).
        decayModes : list of str or None
            List of decay mode strings.

        Returns
        -------
        list of str
            Child isotope codes resulting from each decay mode.
        """
        if decayModes == None: # stable istotope case
            return []
        parentStr = str(parent)
        Z = int(parentStr[0:3])
        A = int(parentStr[3:6])
        meta = parentStr[6:10]
        childIsotopes = []
        for decayMode in decayModes:
            if decayMode == "B-": # beta -
                Z += 1
            elif decayMode == "A": # alpha
                A -= 4
                Z -= 2
            elif decayMode == "EC" or decayMode == "B+": # electron capture
                Z -= 1
            elif decayMode == "EP" : # beta - proton decay
                A -= 1
            elif decayMode == "P": # proton release
                A -= 1
                Z -= 1
            elif decayMode == "SF": # spontaneous fission
                return ["SF"]
            elif decayMode == "IT": # internal transition
                if meta == "0001":
                    meta = "0000"
                elif meta == "0010":
                    meta = "0001"
                else:
                    print(f"Error : metastable state {meta} not valid!")   
            else: # decay mode not defined
                raise ValueError
                #print(f"Error : Decay mode {decayMode} not valid!")
            childIsotopes.append(f"{Z:03}{A:03}{meta}")
        return childIsotopes
    
    def buildDecayDictionary(self, out_fName: str, out_fPath: str):
        """
        Build decay dictionary from ENDF files and save as JSON.

        Reads each decay file, extracts parent, half-life, decay modes,
        and branching probabilities, assembling them into a structured dictionary.

        Output is saved as JSON in './procData/decayData.json'.

        Parameters
        ----------
        out_fName : str
            Output filename (not used, kept for compatibility).
        out_fPath : str
            Output path (not used in this implementation).

        Returns
        -------
        None
        """
        # create empty lists to store data into
        isotopes = []
        halfLives = []
        decayMode = []
        decayProb = []

        HLfails = 0
        AssumedBeta = 0

        # iterate through each file and extract: Parent Isotope, Half life [sec], Decay type
        for fName in self.fNames:
            # read in file as lines
            fPath = os.path.join(self.decayENDF_fPath,fName)
            with open(fPath,'r') as file:
                lines = file.readlines()
            
            # search through lines for key phrases:
            HL = False
            DM = False
            DM_temp = None
            HL_temp = None
            DP_temp = None
            for line in lines:
                # Check for other half life name and change
                if "T1/2=" in line:
                    line = line.replace("T1/2=","Parent half-life: ")
                    #print(f"T1/2 replaced : {line}")

                # check for stable case
                if "Parent half-life:" in line and "STABLE" in line: # stable state
                    DM = True
                    DM_temp = None
                    HL = True
                    HL_temp = "Inf"
                
                elif "Parent half-life:" in line: # normal case
                    HL = True
                    HL_temp = line.strip("Parent half-life:")
                    # remove last 8 characters from string
                    HL_temp = HL_temp[:-10]
                    HL_temp = HL_temp.strip()

                    # convert string into halflife using function
                    try:
                        HL_temp = decayProcessing.convert_to_seconds(HL_temp)
                    except:
                        print(f"Time conversion fail for {fName} @ {HL_temp} ")
                        HL_temp = None
                        HLfails += 1

                if "Decay Mode:" in line and DM == False: # found decay mode and NOT stable
                    DM = True
                    DM_temp = line.strip("Decay Mode:")
                    # remove last 8 characters
                    DM_temp = DM_temp[:-10]
                    DM_temp = DM_temp.strip()
                    DM_tempOG = DM_temp
                    
                    # remove double formating with no probabilities
                    if DM_temp == "A, EC":
                        DM_temp = "A"
                    if DM_temp == "EC, A":
                        DM_temp = 'EC'
                    
                    # add in formats for normal operations
                    if (DM_temp == "B-") or (DM_temp == "A") or (DM_temp == "EC") or (DM_temp == "IT"):
                        DM_temp = DM_temp.replace("B-","B-=100.00%")
                        DM_temp = DM_temp.replace("A","A=100.00%")
                        DM_temp = DM_temp.replace("EC","EC=100.00%")
                        DM_temp = DM_temp.replace("IT","IT=100.00%")
                    
                    # standardize formating
                    DM_temp = DM_temp.replace(" LE ","=")
                    DM_temp = DM_temp.replace(" GT ","=")
                    DM_temp = DM_temp.replace(" AP ","=")
                    DM_temp = DM_temp.replace(" GE ","=")
                    DM_temp = DM_temp.replace(" LT ","=")
                    DM_temp = DM_temp.replace("<","=")
                    DM_temp = DM_temp.replace(">","=")
                    DM_temp = DM_temp.replace("?","")

                    # split data into Decay Modes and Decay Probabilties
                    # Regular expression to match the letter(s) and the percentage
                    pattern = r'([A-Za-z\-]+)=(\d+\.\d+)%'

                    # Find all matches using the regex pattern
                    matches = re.findall(pattern, DM_temp)

                    # Separate the matches into two lists
                    DM_temp = [match[0] for match in matches]
                    DP_temp = [float(match[1]) / 100 for match in matches]
                    if DM_temp == [] and DP_temp == []: print(f"{DM_temp} {DP_temp} : \'{DM_tempOG}\'")
                    

                
            if (HL and DM):
                halfLives.append(HL_temp)
                decayMode.append(DM_temp)
                isotopes.append(decayProcessing.convert_fName_to_AAAZZZMMMM(fName))
                decayProb.append(DP_temp)
                #isotopes.append(fName[4:-5])
            elif (HL is True and DM is False): # Fix broken cases
                # Just assume that it is a B- decay since most errors are from here
                # probably won't cause problems...
                DM_temp = ["B-"] # Nothing has ever gone wrong making assumptions
                DP_temp = [1.0]
                halfLives.append(HL_temp)
                decayMode.append(DM_temp)
                isotopes.append(decayProcessing.convert_fName_to_AAAZZZMMMM(fName))
                decayProb.append(DP_temp)
                #isotopes.append(fName[4:-5])
                if self.consoleLog : print(f"Assumed B- decay for {fName}")
                AssumedBeta += 1
            else:
                if self.consoleLog : print(f"HL DM read fail for {fName} @ HL:{HL_temp} DM:{DM_temp}")
        
        
        # create dictionary for output
        decayDict = {}
        dictFails  = 0
        for i in range(len(isotopes)):
            parent = isotopes[i]
            if halfLives[i] == None : continue # catch error and remove bad data
            try:
                decayDict[parent] = {
                    'decayConst' :  1/float(halfLives[i]),
                    'childNames' : decayProcessing.childIsotopes(parent,decayMode[i]),
                    'childProbs' : decayProb[i]
                    }
            except:
                print(f"DictFail for : {halfLives[i]} {decayMode[i]} {decayProb[i]}")
                dictFails += 1
                continue
            
        
        print("  ***** RUN SUMMARY *****")
        print(f"HL DM read fails      : {len(self.fNames)-len(halfLives)}")
        print(f"Time conversion fails : {HLfails}")
        print(f"Assumed B- decays     : {AssumedBeta}")
        print(f"Decay dictionary fails : {dictFails}")
        
        with open("./procData/decayData.json",'w') as file:
            json.dump(decayDict, file, indent=4)

        # create formatted output file
        #linesOut = []
        #with open("decayData.csv",'w') as file:
        #    for i in range(len(halfLives)):
        #        linesOut.append( f"{isotopes[i]},{halfLives[i]},{decayMode[i]}\n" )
        #    # write output to file
        #    file.writelines(linesOut)

class decayChain:
    """
    Solves for decay chains and decay related things
    """
    def __init__(self,fPath):
        """
        Load decay data dictionary from JSON file.

        Parameters
        ----------
        fPath : str
            Folder containing 'decayData.json'.
        """
        try:
            with open(os.path.join(fPath,"decayData.json"),'r') as decayDataFile:
                self.decayData = json.load(decayDataFile)
        except FileNotFoundError:
            print(f"Error : decayData.json file could not be found at {fPath}")
            
    def decayChain(self,parent: str, depth: int) -> List[str]:
        """
        Stub for recursive decay chain solution.

        Parameters
        ----------
        parent : str
            Parent isotope code.
        depth : int
            Depth to trace down the chain.

        Returns
        -------
        list of str
            Decay chain isotopes (not implemented).
        """
        if not hasattr(self,self.decayData):
            print("Error : decayData not found!")
        
        decayList = []
        n = 0
        while n < depth:
            for isotope in decayList:
                pass

# setup for auto script
if __name__ == '__main__':
    decay = decayProcessing('./rawData/ENDF-B-VIII.0/decay',consoleLog=True)
    decay.buildDecayDictionary("test","test")
    
    
