"Module to plot results from reactor solver"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plotHistogram(history,isotopes,runlabels,fName):
    fig,ax = plt.subplots()
    # parse data by column for each data type
    bottom = np.zeros(history.shape[0])
    for i in range(history.shape[1]):
        data = history[:,i]
        ax.bar(runlabels,data,bottom=bottom,label=isotopes[i])
        bottom += data # update bottom of data range
        label = []
    
    box = ax.get_position()
    ax.set_ylim(.9,1)
    ax.set_ylabel("Fuel Composition")
    ax.set_title("Fuel Composition Evolution")
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=4)
    fig.savefig(f'{fName}.png',dpi=600)
    
        
    
def plotLinegraph(history,isotopes,fName):
    pass

# testing (remove from final prodution)
if __name__ == '__main__':
    iso = ['U238','U235','Pu','FP']
    labels= ['New UO2 fuel','LWR  UO2 SNF','PUREX Out (MOX)','LWR MOX SNF']
    # each row is new set of data
    history = np.array([[.97,.03,0,0],
                        [.95,.01,.01,.03],
                        [.95,.02,.03,0],
                        [.93,.005,.015,.05]])
    plotHistogram(history,iso,labels,"fuelCycleHistogram")
    