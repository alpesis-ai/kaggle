#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 1 2014
#-----------------------------------------------------------#


dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def splitUnit(data, name):
    for unit in set(data['unit']):
        unitData = data[data['unit'] == unit]
        unitData.to_csv(dataPath + "unit\\" + name + "-" + str(unit) + ".csv")

def main():
    
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    train = train[train['Year'] > 2010]

    splitUnit(train, "train")
    splitUnit(test, "test")



if __name__ == "__main__":
    main()
