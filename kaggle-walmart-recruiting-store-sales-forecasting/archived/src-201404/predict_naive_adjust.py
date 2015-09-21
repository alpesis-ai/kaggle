#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 4 2014
#-----------------------------------------------------------#

'''
thisSales = lastSales + corr * mean
- (recent) lastSales: 2012
- (trend) mean/corr: 2011-2012
'''


dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def createPeriod(data):
    data['Period'] = data['Month'] * 10 + data['Week']
    data['id'] = data['unit'].astype(str) + "_" + data['Period'].astype(str)
    return data

def sampleTwoPeriods(train):
    return train[train['Year'] > 2010]

def sampleLastPeriod(train):
    train2011 = train[train['Year'] == 2011]
    train2011 = train2011[train2011['Month'] > 10]

    train2012 = train[train['Year'] == 2012]

    trainLast = pd.concat([train2011, train2012], axis=0)
    return trainLast

def calPeriodMean(train):
    train = train.loc[:, ['unit', 'id', 'Weekly_Sales']]
    periodMeans = train.groupby(['unit', 'id']).mean().reset_index()
    return periodMeans

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

    return salesCorr

def calCorrMeans(periodMeans, salesCorr):
    corrMeans = pd.merge(periodMeans, salesCorr, left_on='unit', right_on='unit', how='left')
    corrMeans['corrMean'] = corrMeans['corr'] * corrMeans['Weekly_Sales']
    
    corrMeans0 = corrMeans[corrMeans['corr'] == 0]
    corrMeans1 = corrMeans[corrMeans['corr'] > 0]
    corrMeans2 = corrMeans[corrMeans['corr'] < 0]

    corrMeans0['index'] = 0
    corrMeans1['index'] = 1.1
    corrMeans2['index'] = 0.9

    corrMeans = pd.concat([corrMeans0, corrMeans1, corrMeans2], axis=0)
    
    return corrMeans

def predict(corrMeans, periodMeanLast):
    corrMeans = corrMeans.loc[:, ['id', 'index']]
    periodMeanLast = periodMeanLast.loc[:, ['id', 'Weekly_Sales']]

    results = pd.merge(periodMeanLast, corrMeans, left_on='id', right_on='id', how='left')
    results['pred'] = results['Weekly_Sales'] * results['index']
    return results

def mergeTest(test, results):
    results = results.loc[:, ['id', 'pred']]
    test = test.loc[:, ['Store', 'Dept', 'Date', 'id']]
    test['Id'] = test['Store'].astype(str) + "_" + test['Dept'].astype(str) + "_" + test['Date'].astype(str)

    submissions = pd.merge(test, results, left_on='id', right_on='id', how='left')
    submissions = submissions.loc[:, ['Id', 'pred']]
    submissions = submissions.rename(columns={'pred': 'Weekly_Sales'})
    submissions['Weekly_Sales'] = submissions['Weekly_Sales'].fillna(0)
    return submissions

def main():
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    train = createPeriod(train)
    test = createPeriod(test)

    train = sampleTwoPeriods(train)
    trainLast = sampleLastPeriod(train)

    periodMeans = calPeriodMean(train)
    periodMeanLast = calPeriodMean(trainLast)

    salesCorr = calUnitCorr(train)
    corrMeans = calCorrMeans(periodMeans, salesCorr)

    results = predict(corrMeans, periodMeanLast)
    submissions = mergeTest(test, results)
    submissions.to_csv(tempPath)




if __name__ == "__main__":
    main()

