import openmc
from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt
import re

u235yields = openmc.data.FissionProductYields('nfy-092_U_235.endf')

# Function written by ChatGPT
def remove_letters(isotope):
    return re.sub(r'[^0-9]', '', isotope)

#Nkeys = print(len(u235yields.independent[1]))
isotopeList = []
yieldList = []
A_yieldList = np.zeros(200)

# repeate code for 3 different energy i levels?

print(u235yields.independent[0].keys())

for key in u235yields.independent[0]:
    # check if value above certain significance 
    if 1 > 0 : # u235yields.independent[0][key].nominal_value > 0:
        yieldList.append(u235yields.independent[0][key].nominal_value)
        isotopeList.append(key)

for key in u235yields.independent[1]:
    # check if value above certain significance 
    if 1 > 0 : # u235yields.independent[1][key].nominal_value > 0:
        yieldList.append(u235yields.independent[1][key].nominal_value)
        isotopeList.append(key)

for key in u235yields.independent[2]:
    # check if value above certain significance 
    if 1 > 0 : #u235yields.independent[2][key].nominal_value > 0:
        yieldList.append(u235yields.independent[2][key].nominal_value)
        isotopeList.append(key)

with open("isotopeList.txt",'w') as f:
    for index,key in enumerate(isotopeList):
        i = int(remove_letters(key))
        #print(i)
        if i > 200:
            continue
        A_yieldList[i] += yieldList[i]
        print((str(isotopeList[i]))+"     "+str(yieldList[i]),file=f)
        #f.write(str(isotopeList[i]))+"     "+str(yieldList[i])


plt.plot(A_yieldList)
plt.show()