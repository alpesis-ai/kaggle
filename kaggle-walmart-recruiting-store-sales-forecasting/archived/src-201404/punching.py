#------------------------------------------------------------------#
# Project: Walmart Store Sales Forecasting
# Author: Kelly Chan
# Date: Mar 24 2014 
#------------------------------------------------------------------#

dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\data\\"
outPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\" 

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def mergeStore(train, store):
    table = pd.merge(train, store, left_on="Store", \
                                   right_on="Store", \
                                   how="left")
    return table


def mergeFeature(fullData, feature):
    table = pd.merge(fullData, feature, left_on=["Store", "Date", "IsHoliday"], \
                                        right_on=["Store", "Date", "IsHoliday"], \
                                        how="left")
    return table


def cleanHoliday(fullData):
    boolDict = {True: 1, False: 0}
    fullData['IsHoliday'] = fullData['IsHoliday'].map(boolDict)

    return fullData

def cleanStoreType(fullData):
    typeDict = {'A': 1, 'B': 2, 'C': 3}
    fullData['Type'] = fullData['Type'].map(typeDict)
    return fullData

def createUnit(fullData):
    fullData['Store'] = fullData['Store'].astype(str)
    fullData['Dept'] = fullData['Dept'].astype(str)
    fullData['unit'] = fullData['Store'] + "_" + fullData['Dept']
    return fullData


def splitDate(fullData):

    colYear = []
    colMonth = []
    colDate = []
    colWeek = []

    fullData['Date'] = fullData['Date'].astype(str)
    for date in fullData['Date']:
        year, month, date = date.split('-')

        date = int(date)
        if (1 <= date <= 7):
            week = 1
        elif (8 <= date <= 14):
            week = 2
        elif (15 <= date <= 21):
            week = 3
        elif (22 <= date <= 28):
            week = 4
        elif (29 <= date <= 31):
            week = 5

        colYear.append(year)
        colMonth.append(month)
        colDate.append(date)
        colWeek.append(week)

    fullData['Year'] = colYear
    fullData['Month'] = colMonth
    fullData['nDate'] = colDate
    fullData['Week'] = colWeek
        
    return fullData

def createData(data, store, feature):
    fullData = mergeStore(data, store)
    fullData = mergeFeature(fullData, feature)

    fullData = cleanHoliday(fullData)
    fullData = cleanStoreType(fullData)
    fullData = createUnit(fullData)
    fullData = splitDate(fullData)

    return fullData

def main():

    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")
    store = loadData(dataPath + "stores.csv")
    feature = loadData(dataPath + "features.csv")

    cleanTrain = createData(train, store, feature)
    cleanTest = createData(test, store, feature)

    cleanTrain.to_csv(outPath + "train.csv")
    cleanTest.to_csv(outPath + "test.csv")

    

if __name__ == "__main__":
    main()
