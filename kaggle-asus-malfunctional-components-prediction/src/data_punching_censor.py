#---------------------------------------------------------#
# Project: ASUS - data punching (censor)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import pandas as pd

def dataLoad(datafile):
    return pd.read_csv(datafile)

def createCensor(repairTrain, saleTrain):
    failData = repairTrain.loc[:, ['unit', 'betweenMonths']]
    failData['state'] = 'F'

    suspendData = saleTrain.loc[:, ['unit', 'betweenMonths']]
    suspendData['state'] = 'S'

    censorData = pd.concat([failData, suspendData], axis=0)
    censorData = censorData.sort(columns=['unit', 'betweenMonths'], ascending=[True, True])
    censorData = censorData.drop_duplicates(['unit', 'betweenMonths', 'state'])
    censorData = censorData.set_index('unit')

    return censorData


def outCSV(data, outPath):
    return data.to_csv(outPath)

def test():
    salePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-saleTrain.csv"
    repairPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-repairTrain.csv"
    sale = dataLoad(salePath)
    repair = dataLoad(repairPath)

    outPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\censor.csv"
    censor = createCensor(repair, sale)
    outCSV(censor, outPath)

test()
