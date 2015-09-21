#---------------------------------------------------------#
# Project: ASUS - return prediction
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

from scipy import stats
import pandas as pd
import numpy as np
import csv

def loadData(datafile):
    return pd.read_csv(datafile)

def predict(samples):
    samples['numRepair'] = samples['numSale'] * samples['returnRate']
    samples['numRepair'] = samples['numRepair'].astype(int)
    
    return samples

def sumPredict(predTable):
    predTable = predTable.loc[:, ['unit', 'predDate', 'numRepair']]
    predTable = predTable.groupby(['unit', 'predDate']).sum()
    predTable = predTable.reset_index()


    #predTable = predTable.loc[:, 'unit', 'predDate', 'numRepair']
    #predTable = predTable.reindex(columns=['unit', 'predDate', 'numRepair'])
    return predTable


def combineID(predTable, idTable):

    table = pd.merge(idTable, predTable, left_on=['unit', 'predDate'], \
                                         right_on = ['unit', 'predDate'], \
                                         how = 'left')
    return table


def test():
    idPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-samples.csv"
    samplesPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\predict-samples.csv"
    
    idTable = loadData(idPath)
    idTable = idTable.loc[:, ['id', 'unit', 'predDate']]

    samples = loadData(samplesPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\predict.csv"
    predTable = predict(samples)
    predTable.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\predict-final.csv"
    finalPredict = sumPredict(predTable)
    finalPredict.to_csv(outPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\tables\\final-id.csv"
    finalID = combineID(finalPredict, idTable)
    finalID.to_csv(outPath)

test()

