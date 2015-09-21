#-------------------------------------------------------#
# Project: ASUS
# Author: Kelly Chan
# Date: Mar 29 2014
#-------------------------------------------------------#

dataPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\"
outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\temp.csv"

import numpy as np
import pandas as pd
from ggplot import *

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(10)

def calModuleRepair(repair):
    repair = repair.loc[:, ['module', 'numRepair']]
    return repair.groupby('module').sum().reset_index()

def calModuleSales(sale):
    sale = sale.loc[:, ['module', 'numSale']]
    return sale.groupby('module').sum().reset_index()

def mergeModule(moduleSales, moduleRepair):
    summary = pd.merge(moduleSales, moduleRepair, left_on='module', \
                                                  right_on='module', \
                                                  how='left')
    summary['returnRate'] = summary['numRepair'] / summary['numSale'].astype(float)
    return summary

def calComponentRepair(repair):
    repair = repair.loc[:, ['component', 'numRepair']]
    return repair.groupby('component').sum().reset_index()

def calComponentSales(sale):
    sale = sale.loc[:, ['component', 'numSale']]
    return sale.groupby('component').sum().reset_index()

def mergeComponents(componentSales, componentRepair):
    summary = pd.merge(componentSales, componentRepair, left_on='component', \
                                                        right_on='component', \
                                                        how='left')
    summary['returnRate'] = summary['numRepair'] / summary['numSale'].astype(float)
    return summary

def genHeavyMal(componentSummary):
    heavyMal = componentSummary[componentSummary['numRepair'] > 100]
    return sorted(set(heavyMal['component']))

def genLightMal(componentSummary):
    lightMal = componentSummary[componentSummary['numRepair'] <= 100]
    lightMal = lightMal[lightMal['numRepair'] > 2]
    return sorted(set(lightMal['component']))

def genNoMal(componentSummary):
    noMal = componentSummary[componentSummary['numRepair'] < 3]
    return sorted(set(noMal['component']))

def viewLightComps(lightComps, repair):
    for comp in lightComps:
        compData = repair[repair['component'] == comp]
        print comp, len(compData), sorted(set(compData['module']))
        print compData.groupby('module').sum()

def main():

    sale = loadData(dataPath + "clean-saleTrain.csv")
    repair = loadData(dataPath + "clean-repairTrain.csv")
    samples = loadData(dataPath + "clean-samples.csv")

    moduleRepair = calModuleRepair(repair)
    moduleSales = calModuleSales(sale)
    moduleSummary = mergeModule(moduleSales, moduleRepair)

    componentRepair = calComponentRepair(repair)
    componentSales = calComponentSales(sale)
    componentSummary = mergeComponents(componentSales, componentRepair)

    heavyComps = genHeavyMal(componentSummary)
    lightComps = genLightMal(componentSummary)
    goodComps = genNoMal(componentSummary)

    viewLightComps(lightComps, repair)
    



if __name__ == "__main__":
    main()
