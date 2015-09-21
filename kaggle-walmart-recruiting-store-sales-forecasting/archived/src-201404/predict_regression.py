#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 1 2014
#-----------------------------------------------------------#


dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np
from sklearn import linear_model


def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def fillNA(data):
    return data.fillna(0)


def createRegression(train):
    clf = linear_model.LinearRegression()
    clf.fit(train.loc[:, ['IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',\
                          'Temperature', 'Month', 'Week']], 
            train.loc[:, ['Weekly_Sales']])
    return clf

def predictRegression(clf, test):

    test['Weekly_Sales'] = clf.predict(test.loc[:,  ['IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', \
                                                     'Temperature', 'Month', 'Week']])
    test['Id'] = test['unit'] + "_" + test['Date']
    submissions = test.loc[:, ['Id', 'Weekly_Sales']]
    submissions = submissions.fillna(0)

    return submissions

def predictUnits(train, test):

    results = pd.DataFrame()
    for unit in set(test['unit']):
        unitTrain = train[train['unit'] == unit].reset_index()
        unitTest = test[test['unit'] == unit].reset_index()

        if len(unitTrain) > 10:
            clf = createRegression(unitTrain)
            submissions = predictRegression(clf, unitTest)
        else:
            unitTest['Id'] = unitTest['unit'] + "_" + unitTest['Date']
            submissions = unitTest.loc[:, ['Id']]
            submissions['Weekly_Sales'] = 0

        results = pd.concat([results, submissions], axis=0)

    results0 = results[results['Weekly_Sales'] > 0].reset_index()
    results1 = results[results['Weekly_Sales'] <= 0].reset_index()
    results1 = results1.loc[:, ['Id']]
    results1['Weekly_Sales'] = 0
    submissions = pd.concat([results0, results1], axis=0)

    return submissions


def predictCSV(test):

    results = pd.DataFrame()
    for unit in set(test['unit']):
        unitTrain = loadData(dataPath + "unit\\train-" + str(unit) + ".csv")
        unitTest = loadData(dataPath + "unit\\test-" + str(unit) + ".csv")

        unitTrain = fillNA(unitTrain)
        unitTest = fillNA(unitTest)

        if len(unitTrain) > 5:
            clf = createRegression(unitTrain)
            submissions = predictRegression(clf, unitTest)
        else:
            unitTest['Id'] = unitTest['unit'] + "_" + unitTest['Date']
            submissions = unitTest.loc[:, ['Id']]
            submissions['Weekly_Sales'] = 0

        results = pd.concat([results, submissions], axis=0)

    results0 = results[results['Weekly_Sales'] > 0]
    results1 = results[results['Weekly_Sales'] <= 0]
    results1 = results1.loc[:, ['Id']]
    results1['Weekly_Sales'] = 0
    submissions = pd.concat([results0, results1], axis=0)

    return submissions



def main():
    
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    train = train[train['Year'] > 2010]
    #train['IsHoliday'] = train['IsHoliday'] * 1000

    train = fillNA(train)
    test = fillNA(test)

    #clf = createRegression(train)
    #submissions = predictRegression(clf, test)
    #submissions.to_csv(tempPath)
    
    submissions = predictUnits(train, test)
    submissions.to_csv(tempPath)

    #results = predictCSV(test)
    #results.to_csv(tempPath)



if __name__ == "__main__":
    main()
