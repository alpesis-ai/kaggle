#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 1 2014
#-----------------------------------------------------------#


dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\"
tablePath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\tables\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def calStoreSales(train):
    train = train.loc[:, ['Store', 'Weekly_Sales']]
    storeTotalSales = train.groupby('Store').sum().reset_index()
    storeMeanSales = train.groupby('Store').mean().reset_index()

    storeSales = pd.merge(storeTotalSales, storeMeanSales, left_on='Store', \
                                                           right_on='Store', \
                                                           how='left')

    storeSales = storeSales.rename(columns={'Weekly_Sales_x': 'TotalSales', \
                                            'Weekly_Sales_y': 'MeanSales'})

    storeSales['N'] = storeSales['TotalSales'] / storeSales['MeanSales']

    storeSales.to_csv(tablePath + "stat\\storeSales.csv")
    return storeSales

def calDeptSales(train):
    train = train.loc[:, ['Dept', 'Weekly_Sales']]
    deptTotalSales = train.groupby('Dept').sum().reset_index()
    deptMeanSales = train.groupby('Dept').mean().reset_index()

    deptSales = pd.merge(deptTotalSales, deptMeanSales, left_on='Dept', \
                                                           right_on='Dept', \
                                                           how='left')

    deptSales = deptSales.rename(columns={'Weekly_Sales_x': 'TotalSales', \
                                            'Weekly_Sales_y': 'MeanSales'})

    deptSales['N'] = deptSales['TotalSales'] / deptSales['MeanSales']

    deptSales.to_csv(tablePath + "stat\\deptSales.csv")
    return deptSales

def calUnitCorr(train):
    train = train.loc[:, ['unit', 'Weekly_Sales', 'Year', 'Month', 'Week']]
    train['Period'] = train['Year'] * 1000 + train['Month'] * 10 + train['Week']

    units = []
    corrs = []
    for unit in set(train['unit']):
        unitData = train[train['unit'] == unit]
        thisCorr = unitData['Weekly_Sales'].corr(unitData['Period'])
        units.append(unit)
        corrs.append(thisCorr)

    salesCorr = pd.DataFrame({'unit': units, 'corr': corrs})
    salesCorr = salesCorr.sort(columns=['unit', 'corr'])
    salesCorr = salesCorr.reindex(columns=['unit', 'corr'])
    salesCorr = salesCorr.fillna(0)

    salesCorr.to_csv(tablePath + "stat\\salesCorr.csv")
    return salesCorr

def calMonthCorr(train):
    train = train.loc[:, ['unit', 'Weekly_Sales', 'Month']]

    units = []
    corrs = []
    for unit in set(train['unit']):
        unitData = train[train['unit'] == unit]
        thisCorr = unitData['Weekly_Sales'].corr(unitData['Month'])
        units.append(unit)
        corrs.append(thisCorr)

    monthCorr = pd.DataFrame({'unit': units, 'corr': corrs})
    monthCorr = monthCorr.sort(columns=['unit', 'corr'])
    monthCorr = monthCorr.reindex(columns=['unit', 'corr'])
    #monthCorr = monthCorr.fillna(0)

    monthCorr.to_csv(tablePath + "stat\\monthCorr.csv")
    return monthCorr

def main():
    
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    #storeSales = calStoreSales(train)
    #deptSales = calDeptSales(train)    
    #salesCorr = calUnitCorr(train)
    monthCorr = calMonthCorr(train)



if __name__ == "__main__":
    main()
