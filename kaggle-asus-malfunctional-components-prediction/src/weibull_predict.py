#---------------------------------------------------------#
# Project: ASUS - weibull distrition (return prediction)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import pandas as pd
import numpy as np
import math

def dataLoad(datafile):
    return pd.read_csv(datafile)

# R: reliability
# R(t, eta, beta) = e^(-(t/eta)^beta)
def R(t, eta, beta):
    ratio = float(t) / eta
    z = math.pow(ratio, beta)
    R = math.exp(-z) # R: reliability
    return R

def predict(unit, eta, beta, saleTrain, repairTrain, samples):

    for index in saleTrain.index:

        saleTotal = saleTrain.iloc[index, 4] # index, 0, unit, saleDate, numSale

        saleDate = saleTrain.iloc[index, 3]
        saleDate = pd.to_datetime(saleDate)

        for testDate in samples['predDate']:

            testDate = pd.to_datetime(testDate)
            betweenMonths = (testDate.year * 12 - (12 - testDate.month)) - \
                            (saleDate.year * 12 - (12 - saleDate.month))

            t0 = betweenMonths + 1
            t1 = t0 + 1
            prob = 1 - R(t1, eta, beta) / R(t0, eta, beta)

            returnData = repairTrain[repairTrain['saleDate'] == saleDate]
            returnTotal = returnData['numRepair'].sum()
            suspended = saleTotal - returnTotal

            thisReturn = int(suspended * prob) # NOTE: int? round?

            record = ["0", "0", unit, saleDate, testDate, thisReturn]

            repairN = len(repairTrain)
            repairTrain.loc[repairN+1] = record

    return repairTrain

def sumPredict(samples, predRepair, outPath):

    for id in samples['id']:
        unit = samples.iloc[id-1, 3]
        testDate = samples.iloc[id-1, 4]
        testDate = pd.to_datetime(testDate)

        predRepair = predRepair[predRepair['unit'] == unit]
        predData = predRepair[predRepair['repairDate'] == testDate]
        samples.iloc[id-1, 5] = predData['numRepair'].sum()

    samples.to_csv(outPath)

    return samples

def test():

    salePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\sales-summary.csv"
    repairPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\repair-summary.csv"
    weibullPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-weibull.csv"
    #samplesPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-samples.csv"
    samplesPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-small-samples.csv"

    saleSum = dataLoad(salePath)
    repair = dataLoad(repairPath)
    weibull = dataLoad(weibullPath)
    samples = dataLoad(samplesPath)

#    beta = 1.23
#    eta = 34.8
#    unitSale = saleSum[saleSum['unit'] == "M7P22"]
#    unitRepair = repair[repair['unit'] == "M7P22"]
#    unitSamples = samples[samples['unit'] == "M7P22"]

#    unitSale = unitSale.reset_index('unit')
#    unitRepair = unitRepair.reset_index('unit')
    
#    unitPred = predict("M7P22", eta, beta, unitSale, unitRepair, unitSamples)
#    print unitPred
    #temp = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\temp.csv"
    #unitPred.to_csv(temp)


    fullPred = pd.DataFrame()

    for unit in set(samples['unit']):

        unitWei = weibull[weibull['unit'] == unit]
        if len(unitWei) == 1:
            beta = unitWei.iloc[0,1]
            eta = unitWei.iloc[0,2]
            
            unitSale = saleSum[saleSum['unit'] == unit]
            unitRepair = repair[repair['unit'] == unit]
            unitSamples = samples[samples['unit'] == unit]  

            unitSale = unitSale.reset_index('unit')
            unitRepair = unitRepair.reset_index('unit')

            unitPred = predict(unit, eta, beta, unitSale, unitRepair, unitSamples)

            fullPred = pd.concat([fullPred, unitPred], axis=0)
            

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\predict.csv"
    fullPred.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\predict-summary.csv"
    sumPredict(samples, fullPred, outPath)
       
 

test()
