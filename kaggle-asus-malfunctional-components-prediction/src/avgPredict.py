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

def calMonthlySales(sale):
    sale = sale.loc[:, ['unit', 'saleDate', 'numSale']]

    monthlySales = sale.groupby(['unit', 'saleDate']).sum()
    monthlySales = monthlySales.reset_index()
    return monthlySales

def calMonthlyRepair(repair):
    repair = repair.loc[:, ['unit', 'saleDate', 'betweenMonths', 'numRepair']]
    
    monthlyRepair = repair.groupby(['unit', 'saleDate', 'betweenMonths']).sum()
    monthlyRepair = monthlyRepair.reset_index()
    return monthlyRepair

def mergeRepairSale(monthlyRepair, monthlySale):
    summary = pd.merge(monthlyRepair, monthlySale, left_on=['unit', 'saleDate'], \
                                                   right_on=['unit', 'saleDate'], \
                                                   how='left')
    
    # removing numSale == -1
    summary = summary[summary['numSale'] > 0]
    summary = summary.reindex(columns=['unit', 'saleDate', 'numSale', 'betweenMonths', 'numRepair'])
    return summary    


def calCorr(summary):
    corrSummary = summary
    corrSummary['id'] = corrSummary['unit'] + "-" + corrSummary['saleDate']
    corrSummary = corrSummary.loc[:, ['id', 'numSale', 'betweenMonths', 'numRepair']]

    unitDateList = []
    minMonthList = []
    maxMonthList = []
    meanMonthList = []
    minRepairList = []
    maxRepairList = []
    meanRepairList = []
    totalRepairList = []
    corrRepMonthList = []
    for unitDate in set(corrSummary['id']):
        unitData = corrSummary[corrSummary['id'] == unitDate]

        monthlySale = unitData['numSale'].mean()
        minMonth = unitData['betweenMonths'].min()
        maxMonth = unitData['betweenMonths'].max()
        meanMonth = unitData['betweenMonths'].mean()
        minRepair = unitData['numRepair'].min()
        maxRepair = unitData['numRepair'].max()
        meanRepair = unitData['numRepair'].mean()
        totalRepair = unitData['numRepair'].sum()
        corrRepMonth = unitData.corr(method='pearson', min_periods=1).iloc[2, 1]

        unitDateList.append(unitDate)
        minMonthList.append(minMonth)
        maxMonthList.append(maxMonth)
        meanMonthList.append(meanMonth)
        minRepairList.append(minRepair)
        maxRepairList.append(maxRepair)
        meanRepairList.append(meanRepair)
        totalRepairList.append(totalRepair)
        corrRepMonthList.append(corrRepMonth)
    
    corrTable = pd.DataFrame({'id': unitDateList, \
                              'minMonth': minMonthList, \
                              'maxMonth': maxMonthList, \
                              'meanMonth': meanMonthList, \
                              'minRepair': minRepairList, \
                              'maxRepair': maxRepairList, \
                              'meanRepair': meanRepairList, \
                              'totalRepair': totalRepairList, \
                              'corrRepMonth': corrRepMonthList})

    corrTable = corrTable.sort(columns=['id', \
                                           'minMonth', 'maxMonth', 'meanMonth', \
                                           'minRepair', 'maxRepair', 'meanRepair', 'totalRepair', \
                                           'corrRepMonth'])
    corrTable = corrTable.reindex(columns=['id', \
                                           'minMonth', 'maxMonth', 'meanMonth', \
                                           'minRepair', 'maxRepair', 'meanRepair', 'totalRepair', \
                                           'corrRepMonth'])

    corrTable.to_csv(dataPath + "stat.csv")
    return corrTable
    

def trainReturns(summary):
    summary = summary.loc[:, ['unit', 'saleDate', 'betweenMonths', 'numRepair']]

    train = pd.DataFrame()
    for unit in set(summary['unit']):
        unitData = summary[summary['unit'] == unit]

        unitList = []
        datesList = []
        monthList = []
        for saleDate in set(summary['saleDate']):
            for month in range(1,85):
                unitList.append(unit)
                datesList.append(saleDate)
                monthList.append(month)

        unitTable = pd.DataFrame({'unit': unitList, \
                                  'saleDate': datesList, \
                                  'betweenMonths': monthList})
        train = pd.concat([train, unitTable], axis=0)

    train = train.reindex(columns=['unit', 'saleDate', 'betweenMonths'])
    train = pd.merge(train, summary, left_on=['unit', 'saleDate', 'betweenMonths'], \
                                     right_on=['unit', 'saleDate', 'betweenMonths'], \
                                     how='left')
    train = train.fillna(0)

    train['finalReturns'] = train['numRepair']
    returns = pd.DataFrame()
    for i in range(0,len(train),83):
        unitData = train[i:i+84]
        for row in range(2,len(unitData)):
            unitData.loc[row, 'finalReturns'] = 0.5 * (train.loc[row-1, 'numRepair'] + train.loc[row-2, 'numRepair'])
            returns = pd.concat([returns, unitData], axis=0)

    returns['numReturns'] = returns['numReturns'].astype(int)
    returns.to_csv(tempPath)
    print returns.head(10)
    return returns


def main():

    sale = loadData(dataPath + "clean-saleTrain.csv")
    repair = loadData(dataPath + "clean-repairTrain.csv")
    samples = loadData(dataPath + "clean-samples.csv")

    monthlySales = calMonthlySales(sale)
    monthlyRepair = calMonthlyRepair(repair)
    summary = mergeRepairSale(monthlyRepair, monthlySales)
    summary.to_csv(dataPath + "summary.csv")

    #corrTable = calCorr(summary)

    trainReturns(summary)




if __name__ == "__main__":
    main()
