#---------------------------------------------------------#
# Project: ASUS - Data Punching (prediction)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def addPreDates(sale):

    dates = []
    for year in range(2010, 2012):
        for month in range(1, 13):
            date = str(year) + "/" + str(month)
            dates.append(date)
    predDates = pd.DataFrame({'predDate': dates})

    samples = pd.DataFrame()
    for i in range(len(sale)):
        samples = pd.concat([samples, predDates], axis=0)
    samples = samples.reset_index()

    saleCopy = pd.DataFrame()
    for i in range(len(predDates)):
        saleCopy = pd.concat([saleCopy, sale], axis=0)
    saleCopy = saleCopy.sort(columns=['unit', 'saleDate'])
    saleCopy = saleCopy.reset_index()
    
    table = pd.concat([saleCopy, samples], axis=1)
    table = table.loc[:, ['unit', 'saleDate', 'numSale', 'predDate']]
    table = table.reindex(columns=['unit', 'saleDate', 'numSale', 'predDate'])

    #print len(sale)
    #print len(predDates)
    #print len(sale) * len(predDates)
    #print len(table)

    return table

def calBetweenMonths(predTable):

    startDates = predTable['saleDate']
    endDates = predTable['predDate']

    betweenMonths = []
    for i in range(len(startDates)):
        startDate = pd.to_datetime(startDates[i])
        endDate = pd.to_datetime(endDates[i])

        months = (endDate.year * 12 - (12 - endDate.month)) - \
                 (startDate.year * 12 - (12 - startDate.month))
        months = months + 1
        betweenMonths.append(months)

    predTable['betweenMonths'] = betweenMonths
    return predTable


def addReturnRate(predTable, rateTable):

    table = pd.merge(predTable, rateTable, left_on=['unit', 'betweenMonths'], \
                                           right_on=['unit', 'betweenMonths'], \
                                           how='left')
    table = table.fillna(0)
    return table
                                           


def test():
    salePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\sales-summary.csv"
    ratePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\final-returnRate.csv"
    samplePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-samples.csv"

    returnRate = loadData(ratePath)
    sale = loadData(salePath)
    samples = loadData(samplePath)

    sale = sale[sale['numSale'] > 0]

    returnRate = returnRate.loc[:, ['unit', 'betweenMonths', 'returnRate']]
    sale = sale.loc[:, ['unit', 'saleDate', 'numSale']]
    samples = samples.loc[:, ['unit', 'predDate']]    

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\predict-samples.csv"
    predTable = addPreDates(sale)
    predTable= calBetweenMonths(predTable)
    predTable = addReturnRate(predTable, returnRate)
    predTable.to_csv(outPath)



test()
