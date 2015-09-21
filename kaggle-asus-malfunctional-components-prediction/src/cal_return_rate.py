#---------------------------------------------------------#
# Project: ASUS - data punching (summary)
# Author: Kelly Chan
# Date: Mar 26 2014
#---------------------------------------------------------#

import pandas as pd

def loadData(datafile):
    return pd.read_csv(datafile)


def removeNoSales(suspend, repair):
    suspend = suspend.loc[:, ['unit', 'saleDate', 'numSale']]
    missing = suspend[suspend['numSale'] == 0]
    repair = repair.loc[:, ['unit', 'saleDate', 'repairDate', 'betweenMonths', 'numRepair']]
    table = pd.merge(repair, missing, left_on=['unit', 'saleDate'], \
                                      right_on=['unit', 'saleDate'], \
                                      how='left')

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\errorCases.csv"
    errorCases = table[table['numSale'] == 0]
    errorCases.to_csv(outPath)

    table = table[table['numSale'] != 0]

    return table

def calPeriodRepair(repair):
    repair = repair.loc[:, ['unit', 'betweenMonths', 'numRepair']]
    unitRepair = repair.groupby(['unit', 'betweenMonths']).sum()
    unitRepair = unitRepair.reset_index()
    return unitRepair

def calUnitSales(suspend):
    suspend = suspend.loc[:, ['unit', 'saleDate', 'numSale']]

    sales = pd.DataFrame()
    for unit in set(suspend['unit']):
        unitData = suspend[suspend['unit'] == unit]

        noMissing = unitData[unitData['numSale'] != 0]
        noMissing = noMissing.reset_index()
        meanSale = noMissing.groupby('unit').sum() / float(len(noMissing))
        meanSale = meanSale.reset_index()
        avgSale = meanSale.iloc[0,1]

        missing = unitData[unitData['numSale'] == 0]
        missing = missing.reset_index()
        missing['numSale'] = int(avgSale)

        sales = pd.concat([sales, noMissing, missing], axis=0)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\sales-summary.csv"
    sales = sales[sales['numSale'] > 0]
    sales.to_csv(outPath)

    unitSales = sales.groupby(['unit', 'saleDate']).sum()
    unitSales = unitSales.reset_index()

    return unitSales

def calReturnRate(unitPeriodRepair, unitSales):
    table = pd.merge(unitPeriodRepair, unitSales, left_on='unit', \
                                                  right_on='unit', \
                                                  how='left')
    table['returnRate'] = table['numRepair'] / table['numSale'].astype(float)
    return table

def createRateTable(returnRate):
    rateTable = returnRate.loc[:, ['unit', 'betweenMonths', 'returnRate']]
    return rateTable

def test():
    suspendPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\suspend-summary.csv"
    repairPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-repairTrain.csv"
    suspend = loadData(suspendPath)
    repair = loadData(repairPath)

    #repair = removeNoSales(suspend, repair)
    unitPeriodRepair = calPeriodRepair(repair)
    unitSales = calUnitSales(suspend)
    returnRate = calReturnRate(unitPeriodRepair, unitSales)
    rateTable = createRateTable(returnRate)


    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\final-returnRate.csv"
    rateTable.to_csv(outPath)
    print "rateTable saved"

test()
