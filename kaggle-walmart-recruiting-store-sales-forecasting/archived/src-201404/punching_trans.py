#------------------------------------------------------------------#
# Project: Walmart Store Sales Forecasting
# Author: Kelly Chan
# Date: Mar 24 2014 
#------------------------------------------------------------------#

dataPath = "G:\\vimFiles\\python\\kaggle\\201404-Walmart\\src\\data\\" 

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def transLog(data):
    #data['IsHoliday'] = np.log(data['IsHoliday'])
    data['MarkDown1'] = np.log(data['MarkDown1'])
    data['MarkDown2'] = np.log(data['MarkDown2'])
    data['MarkDown3'] = np.log(data['MarkDown3'])
    data['MarkDown4'] = np.log(data['MarkDown4'])
    data['MarkDown5'] = np.log(data['MarkDown5'])

    data['Temperature'] = np.log(data['Temperature'])
    #data['Month'] = np.log(data['Month'])
    #data['Week'] = np.log(data['Week'])

    #data['log_Weekly_Sales'] = np.log(data['Weekly_Sales'])
    return data
def main():

    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    train = train[train['Weekly_Sales'] > 0]
    train['Weekly_Sales'] = np.log(train['Weekly_Sales'])
    train = transLog(train)
    test = transLog(test)

    train.to_csv(dataPath + "logTrain.csv")
    test.to_csv(dataPath + "logTest.csv")



    

if __name__ == "__main__":
    main()
