#---------------------------------------------------------#
# Project: ASUS
# Author: Kelly Chan
# Date: Mar 26 2014
#---------------------------------------------------------#

dataPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\temp.csv"

import numpy as np
import pylab as pl
import pandas as pd
from ggplot import *


def loadData(datafile):
    return pd.read_csv(datafile)


def createRateData(rate):
    rate = rate.loc[:, ['unit', 'betweenMonths', 'returnRate']]

    units = []
    months = []
    for unit in set(rate['unit']):
        for month in range(1, 61):
            units.append(unit)
            months.append(month)
    rateData = pd.DataFrame({'unit': units, 'betweenMonths': months})
    rateData = rateData.reindex(columns=['unit', 'betweenMonths'])

    rateData = pd.merge(rateData, rate, left_on=['unit', 'betweenMonths'], \
                                        right_on=['unit', 'betweenMonths'], \
                                        how='left')
    rateData = rateData.fillna(0)

    return rateData

def calMeanRate(rateData):

    meanRate = pd.DataFrame()
    for unit in set(rateData['unit']):
        unitData = rateData[rateData['unit'] == unit]

        unitData['rate2'] = unitData['returnRate']
        unitData['rate1'] = unitData['rate2'].shift(1)
        unitData['rate3'] = unitData['rate2'].shift(-1)
        unitData = unitData.fillna(0)

        unitData['meanRate'] = 1./3 * (unitData['rate1'] + unitData['rate2'] + unitData['rate3'])
        unitData['diffRate'] = unitData['returnRate'] - unitData['meanRate']

        meanRate = pd.concat([meanRate, unitData], axis=0)

    meanRate = meanRate.loc[:, ['unit', 'betweenMonths', 'meanRate']]
    meanRate = meanRate.reindex(columns=['unit', 'betweenMonths', 'meanRate'])
    meanRate.columns = ['unit', 'betweenMonths', 'returnRate']

    return meanRate


def main():
    #dataPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\"
    #tempPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\temp.csv"

    ratePath = dataPath + "returnRate-summary.csv"

    rate = loadData(ratePath)
    rateData = createRateData(rate)
    meanRate = calMeanRate(rateData)

    meanRate.to_csv(dataPath + "final-returnRate.csv")



if __name__ == "__main__":
    main()

