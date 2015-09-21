#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 4 2014
#-----------------------------------------------------------#


dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def sampleData(train):
    train2011 = train[train['Year'] == 2011]
    train2011 = train2011[train2011['Month'] > 10]

    train2012 = train[train['Year'] == 2012]

    train = pd.concat([train2011, train2012], axis=0)
    return train

def createPeriod(data):
    data['Period'] = data['Month'] * 10 + data['Week']
    data['id'] = data['unit'].astype(str) + "_" + data['Period'].astype(str)
    return data

def calPeriodMean(train):
    train = train.loc[:, ['id', 'Weekly_Sales']]
    periodMeans = train.groupby('id').mean().reset_index()
    return periodMeans

def predictPeriodMean(test, periodMeans):
    test = test.loc[:, ['Store', 'Dept', 'Date', 'id']]
    results = pd.merge(test, periodMeans, left_on='id', right_on='id', how='left')
    results['Weekly_Sales'] = results['Weekly_Sales'].fillna(0)
    
    results['Id'] = results['Store'].astype(str) + "_" + results['Dept'].astype(str) + "_" + results['Date'].astype(str)
    results = results.loc[:, ['Id', 'Weekly_Sales']]
    return results

def main():
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    train = sampleData(train)
    train = createPeriod(train)
    test = createPeriod(test)
    
    periodMeans = calPeriodMean(train)
    results = predictPeriodMean(test, periodMeans)
    
    results.to_csv(tempPath)


if __name__ == "__main__":
    main()
