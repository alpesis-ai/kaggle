#----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 1 2014
#----------------------------------------------------------#

dataPath = "G:\\vimFiles\\python\\kaggle\\Walmart\\data\\"
outPath = "G:\\vimFiles\\python\\kaggle\\Walmart\\src\\data\\"

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def mapHoliday(test):
    coded = {'True': 1, 'False': 0}
    test['IsHoliday'] = test['IsHoliday'].astype(str).map(coded)
    return test

def main():
    test = loadData(dataPath + "test.csv")

    test = mapHoliday(test)
    test.to_csv(outPath+"test.csv")

if __name__ == "__main__":
    main()
