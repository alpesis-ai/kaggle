#---------------------------------------------------------#
# Project: ASUS - data punching (summary)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import pandas as pd

def loadData(datafile):
    return pd.read_csv(datafile)

def sumSales(saleTrain):
    sale = saleTrain.loc[:, ['unit', 'saleDate', 'numSale']]
    sale = sale.sort(columns=['unit','saleDate'])
    saleSum = sale.groupby(['unit', 'saleDate']).sum()
    saleSum.index.name = 'unit'
    saleSum = saleSum.reset_index()
    return saleSum

def sumRepair(repairTrain):
    repair = repairTrain.loc[:, ['unit', 'saleDate', 'repairDate', 'betweenMonths', 'numRepair']]
    repair['betweenMonths'] = repair['betweenMonths'].astype(str)

    repair = repair.sort(columns=['unit','saleDate', 'repairDate'])
    repairSum = repair.groupby(['unit', 'saleDate', 'repairDate', 'betweenMonths']).sum()
    repairSum.index.name = 'unit'
    repairSum = repairSum.reset_index()
    
    return repairSum

def sumPeriodRepair(repairTrain):
    repair = repairTrain.loc[:, ['unit', 'betweenMonths', 'numRepair']]
    repair = repair.sort(columns=['unit', 'betweenMonths'])
    repairSum = repair.groupby(['unit', 'betweenMonths']).sum()
    repairSum.index.name = 'unit'
    repairSum = repairSum.reset_index()

    return repairSum

def sumSaleDateRepair(repairTrain):
    repair = repairTrain.loc[:, ['unit', 'saleDate', 'numRepair']]
    repair = repair.sort(columns=['unit','saleDate'])
    repairSum = repair.groupby(['unit', 'saleDate']).sum()
    repairSum.index.name = 'unit'
    repairSum = repairSum.reset_index()
    
    return repairSum

def tabSuspend(dataA, dataB):
    table = pd.merge(dataA, dataB, left_on=['unit', 'saleDate'], \
                                   right_on=['unit', 'saleDate'], \
                                   how='outer')
    table = table.sort(columns=['unit', 'saleDate', 'numSale', 'numRepair'])
    table = table.fillna(0)
    table['suspend'] = table['numSale'] - table['numRepair']
    return table

def createUnitSale(saleSummary):
    table = saleSummary.groupby('unit').sum()
    table = table.reset_index()
    return table

def calReturnRate(periodRepair, unitSale):

    fullData = pd.DataFrame()
    for unit in set(periodRepair['unit']):
        unitData = periodRepair[periodRepair['unit'] == unit]
        unitTotalSales = unitSale[unitSale['unit'] == unit]        
        totalSales = unitTotalSales['numSale']
        unitData['returnRate'] = unitData['numRepair'] / float(totalSales)

        fullData = pd.concat([fullData, unitData], axis=0)
    
    fullData = fullData.reindex(columns = ['unit', 'betweenMonths', 'numRepair', 'returnRate'])
    fullData = fullData.sort(columns=['unit', 'betweenMonths', 'numRepair'])
    return fullData


def test():
    salePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-saleTrain.csv"
    repairPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-repairTrain.csv"
    saleTrain = loadData(salePath)
    repairTrain = loadData(repairPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\sales-summary.csv"
    summarySale = sumSales(saleTrain)
    summarySale.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\repair-summary.csv"
    summaryRepair = sumRepair(repairTrain)
    summaryRepair.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\repair-period-summary.csv"
    summaryPeriodRepair = sumPeriodRepair(repairTrain)
    summaryPeriodRepair.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\repair-saleDate-summary.csv"
    summarySaleDateRepair = sumSaleDateRepair(repairTrain)
    summarySaleDateRepair.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\suspend-summary.csv"
    suspend = tabSuspend(summarySale, summarySaleDateRepair)
    suspend.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\sale-units-summary.csv"
    unitSale = createUnitSale(summarySale)
    unitSale.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\returnRate-summary.csv"
    returnRate = calReturnRate(summaryPeriodRepair, unitSale)
    returnRate.to_csv(outPath)


test()
