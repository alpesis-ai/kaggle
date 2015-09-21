#------------------------------------------------------------------#
# Project: Walmart Store Sales Forecasting
# Author: Kelly Chan
# Date: Mar 24 2014 
#------------------------------------------------------------------#

dataPath =  "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\"
picPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\outputs\\pics\\"

import pandas as pd
import numpy as np
from ggplot import *

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def plotScatter(dataset, X, Y, unit, outPath):
    p = ggplot(aes(x=X, y=Y), data=dataset)
    p = p + geom_point()
    p = p + ggtitle("Weekly Sales - " + unit)
    ggsave(p, outPath)
    return p


#NOTE: cost 2 hrs to run
def plotWeeklySales(train):

    for unit in set(train['unit']):
        unitData = train[train['unit'] == unit]
        unitData = unitData.reset_index()
        unitData['Date'] = pd.to_datetime(unitData['Date'])

        outPath = picPath + "unit-sales\\" + str(unit) + ".png"
        plotScatter(unitData, 'Date', 'Weekly_Sales', str(unit), outPath)

def plotDeptWeeklySales(train):
    for dept in set(train['Dept']):
        deptData = train[train['Dept'] == dept].reset_index()
        deptData['Date'] = pd.to_datetime(deptData['Date'])

        outPath = picPath + "dept-sales\\" + str(dept) + ".png"
        plotScatter(deptData, 'Date', 'Weekly_Sales', str(dept), outPath)

def plotDeptWeeklySummary(train):
    for dept in set(train['Dept']):
        deptData = train[train['Dept'] == dept].reset_index()
        deptData = deptData.loc[:, ['Dept', 'Date', 'Weekly_Sales']]
        deptData = deptData.groupby(['Dept', 'Date']).sum().reset_index()
        deptData['Date'] = pd.to_datetime(deptData['Date'])

        outPath = picPath + "dept-sales-summary\\" + str(dept) + ".png"
        plotScatter(deptData, 'Date', 'Weekly_Sales', str(dept), outPath)


def plotLogDeptWeekly(train):
    for dept in set(train['Dept']):
        deptData = train[train['Dept'] == dept].reset_index()
        deptData = deptData.loc[:, ['Dept', 'Date', 'Weekly_Sales']]
        deptData = deptData.groupby(['Dept', 'Date']).sum().reset_index()
        deptData['Log_Sales'] = np.log(deptData['Weekly_Sales'])
        deptData['Date'] = pd.to_datetime(deptData['Date'])

        outPath = picPath + "log-sales-summary\\" + str(dept) + ".png"
        plotScatter(deptData, 'Date', 'Log_Sales', str(dept), outPath)

def test():

    train = loadData(dataPath + "train.csv")
    printData(train)

    #plotWeeklySales(train) #NOTE: cost 2 hrs to run
    #plotDeptWeeklySales(train)
    #plotDeptWeeklySummary(train)
    #plotLogDeptWeekly(train)


test()
