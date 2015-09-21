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

def addDummySales(test):
    test['Weekly_Sales'] = 0
    return test

def sampleData(data):
    return data.loc[:, ['unit', 'Date', 'Weekly_Sales']]
 
def concatData(train, test):
    return pd.concat([train, test], axis=0)

def pivotData(fullData):
    tsData = pd.pivot_table(fullData, values='Weekly_Sales', rows=['unit'], cols=['Date'])
    tsData = tsData.reset_index()
    tsData = tsData.fillna(0)
    return tsData

def main():
    
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    test = addDummySales(test)

    train = sampleData(train)
    test = sampleData(test)

    fullData = concatData(train, test)
    tsData = pivotData(fullData)
    tsData.to_csv(tablePath + "tsData.csv")



if __name__ == "__main__":
    main()
