"File to test transmutation in batemanMatrix.py"

import sys
import os
import matplotlib.pyplot as pyplot
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../dataSolver'))

from batemanMatrix import batemanMatrix

# array of isotopes to be tracked
isotopes = ['0922350000','0922360000','0922370000','0922380000']

BM = batemanMatrix(isotopes)
BM.addTransmutations(1)