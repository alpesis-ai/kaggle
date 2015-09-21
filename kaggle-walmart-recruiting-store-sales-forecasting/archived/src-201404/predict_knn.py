#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 1 2014
#-----------------------------------------------------------#


dataPath = "G:\\vimFiles\\python\\kaggle\\Walmart\\src\\data\\"
tablePath = "G:\\vimFiles\\python\\kaggle\\Walmart\\src\\outputs\\tables\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def trainKNN(train):
    neighbors = KNeighborsClassifier(n_neighbors=1)
    neighbors.fit(train.loc[:, ['IsHoliday', 'Year', 'Month', 'Week']], \
                  train['Weekly_Sales'])
    return neighbors

def predictKNN(neighbors, train, test):

    results = pd.DataFrame()
    for unit in set(test['unit']):
        unitTest = test[test['unit'] == unit]
        unitTrain = train[train['unit'] == unit]

        neighbors = trainKNN(unitTrain)
        unitTest['Weekly_Sales'] = neighbors.predict(unitTest.loc[:, ['IsHoliday', 'Year', 'Month', 'Week']])

        unitTest['Id'] = unitTest['unit'].astype(str) + "_" + unitTest['Date'].astype(str)
        thisResults = unitTest.loc[:, ['Id', 'Weekly_Sales']]
        results = pd.concat([results, thisResults], axis=0)

    return results


def main():
    
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    neighbors = trainKNN(train)
    results = predictKNN(neighbors, train, test)
    results.to_csv(tempPath)



if __name__ == "__main__":
    main()
