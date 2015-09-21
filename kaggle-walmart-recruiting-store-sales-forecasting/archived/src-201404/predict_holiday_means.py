#-----------------------------------------------------------#
# Project: Walmart
# Author: Kelly Chan
# Date: Apr 1 2014
#-----------------------------------------------------------#


dataPath = "G:\\vimFiles\\python\\kaggle\\Walmart\\src\\data\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\Walmart\\src\\outputs\\tables\\temp.csv"

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)


def calSalesMeans(train):
    train = train.loc[:, ['unit', 'Weekly_Sales']]
    means = train.groupby('unit').mean()
    means = means.reset_index()
    return means

def calHolidayMeans(train):
    train = train.loc[:, ['unit', 'Weekly_Sales', 'IsHoliday']]
    holidayMeans = train.groupby(['unit', 'IsHoliday']).mean()
    holidayMeans = holidayMeans.reset_index()
    return holidayMeans


def predictHolidayMean(means, holidayMeans, test):

    test['unit'] = test['Store'].astype(str) + "_" + test['Dept'].astype(str)
    test['Id'] = test['unit'].astype(str) + "_" + test['Date'].astype(str)

    test = pd.merge(test, means, left_on='unit', right_on='unit', how='left')
    test = pd.merge(test, holidayMeans, left_on=['unit', 'IsHoliday'], \
                                        right_on=['unit', 'IsHoliday'], \
                                        how='left')
    test['Weekly_Sales_x'] = test['Weekly_Sales_x'].fillna(0)
    test['Weekly_Sales_y'] = test['Weekly_Sales_y'].fillna(0)

    test['Weekly_Sales'] = 0.7 * test['Weekly_Sales_x'] + 0.3 * test['Weekly_Sales_y']
    results = test.loc[:, ['Id', 'Weekly_Sales']]
    return results


def main():
    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    means = calSalesMeans(train)
    holidayMeans = calHolidayMeans(train)
    results = predictHolidayMean(means, holidayMeans, test)
    results.to_csv(tempPath)

if __name__ == "__main__":
    main()
