#---------------------------------------------------------#
# Project: ASUS - data plot
# Author: Kelly Chan
# Date: Mar 21 2014
#---------------------------------------------------------#

import numpy as np
import pandas as pd
from ggplot import *

def loadData(datafile):
    return pd.read_csv(datafile)

def plotScatter(dataset, X, Y, title, outPath):
    p = ggplot(aes(x=X, y=Y), data=dataset)
    p = p + geom_point()
    p = p + scale_x_continuous(breaks=[x for x in range(0,61,6)]) 
    p = p + ggtitle(title)
    ggsave(p, outPath)
    return p

def plotRepair():
    repairPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\repair-period-summary.csv"
    repair = loadData(repairPath)
    print repair.head(10)

    #unitData = repair[repair['unit'] == "M1P25"]
    #print plotScatter(unitData, 'betweenMonths', 'numRepair', "M1P25")

    path = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\pics\\period-repair\\"
    for unit in set(repair['unit']):
        unitData = repair[repair['unit'] == unit]
        outPath = path + str(unit) + ".png"
        plotScatter(unitData, 'betweenMonths', 'numRepair', str(unit), outPath)

plotRepair()
