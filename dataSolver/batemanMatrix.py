import pyne.data as data
from pyne import nucname
import numpy as np
import csv

# create list of isotopes that are fissionable
fissionable = [922350000,922380000,942390000,942400000,942410000]

FYisotopes = {922350000,922380000}

# search through fission yields to build list of items
for iso in fissionable:
    fPath = "./processedFY/"+str(iso)
    FPs = []
    with open(fPath,'r',newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                try:
                    FPs.append(nucname.id(row[0][:-1]))
                except:
                    print(row)
        FYisotopes.update(FPs)

#print(FYisotopes)
print(len(FYisotopes))

# create starting isotope list
# things found in the fuel
isotopeSet = FYisotopes


# find fission products for components in the fuel
#print(data.half_life(822060000))

isotopeSet = {922380000}

N = 0
while N <= 10: # find 10 levels of decay products
    for isotope in isotopeSet:
        daughterIsotopes = data.decay_children(isotope)
        for iso in daughterIsotopes:
            daughterIsotopes.add(iso)
        #aughterIsotopes.update(daughterIsotopes)
    
    isotopeSet.update(daughterIsotopes) 
    N += 1


#print(isotopeSet)
print(len(isotopeSet))


# no need to solve for the decay chains, data already in place
# sort isotope data in preperation for matrix creation

isotopeSet = list(isotopeSet)
isotopeSet.sort()
print(isotopeSet)

# CREATE BATEMAN MATRIX
rows = []
columns = []
value = []