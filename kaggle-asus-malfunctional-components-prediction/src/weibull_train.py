#---------------------------------------------------------#
# Project: ASUS - Weibull Train (eta, beta, corr)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import pandas as pd
import numpy as np
from scipy import stats
from ggplot import *
import csv


def loadData(datafile):
    return pd.read_csv(datafile)

#a = N + 1 - lastRank
#b = N + 1 - index
#adjusted = a/b
#lastRank + adjusted
def weibullCensored(censData):
    N = len(censData)
    failData = censData[censData['state'] == 'F']

    if len(failData) == 0:
        beta = None
        eta = None
        corrXY = None
    else:
    
        # adjustedRank = lastRank + (N+1-lastRank)/(N+1-index)
        adjustedRanks = []
        lastRank = 0
        for originIndex in failData.index:
            a = N + 1 - lastRank
            b = N + 1 - originIndex
            adjusted = float(a) / b
            thisRank = lastRank + adjusted
            adjustedRanks.append(thisRank)
            lastRank = thisRank

        Y = []
        for rank in adjustedRanks:
            medianRank = (rank - 0.3) / (N + 0.4)
            z = 1.0 / (1.0 - medianRank)
            z = np.log(np.log(z))
            Y.append(z)

        X = np.log(failData['betweenMonths'])

        slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)

        beta = slope
        eta = np.exp(-(float(intercept) / beta))

        corrXY = np.corrcoef(X, Y)

    return beta, eta, corrXY


def weibullCensoredPlot(censData):
    N = len(censData)
    failData = censData[censData['state'] == 'F']
    #print failData
    
    # adjustedRank = lastRank + (N+1-lastRank)/(N+1-index)
    adjustedRanks = []
    lastRank = 0
    for originIndex in failData.index:
        #print originIndex
        a = N + 1 - lastRank
        b = N + 1 - originIndex
        adjusted = float(a) / b
        thisRank = lastRank + adjusted
        adjustedRanks.append(thisRank)
        lastRank = thisRank

    Y = []
    for rank in adjustedRanks:
        medianRank = (rank - 0.3) / (N + 0.4)
        z = 1.0 / (1.0 - medianRank)
        z = np.log(np.log(z))
        Y.append(z)

    X = np.log(failData['betweenMonths'])

    weibull = pd.DataFrame({'X': X, 'Y': Y})
    #print weibull
    p = ggplot(aes(x='X', y='Y'), data=weibull)
    p = p + geom_point()
    p = p + ggtitle("weibull censored data")
    p = p + xlab("ln(t)")
    p = p + ylab("ln[ln[1/(1-adjustMedianRank)]]")
    return p


def test():
    censorPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\censor.csv"
    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\weibull.csv"
    censData = loadData(censorPath)

    #unitCens = censData[censData['unit'] == "M8P16"]
    #unitCens = unitCens.reset_index('unit')
    #print weibullCensored(unitCens)
    #print weibullCensoredPlot(unitCens)


    header = ['unit', 'beta', 'eta', 'corrXY']
    with open(outPath, 'wb') as csvfile:
        outData = csv.writer(csvfile, delimiter = ",")
        outData.writerow(header)

        for unit in set(censData['unit']):
            unitCens = censData[censData['unit'] == unit]
            unitCens = unitCens.reset_index('unit')
            beta, eta, corrXY = weibullCensored(unitCens)

            record = [unit, beta, eta, corrXY]
            outData.writerow(record)
    csvfile.close()

    # excluded 1/2 points and None records
    weibullData = loadData(outPath)
    cleanWeibull = weibullData[weibullData['beta'] > 0]
    cleanWeibull = cleanWeibull.set_index('unit')
    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-weibull.csv"
    cleanWeibull.to_csv(outPath)


test()
