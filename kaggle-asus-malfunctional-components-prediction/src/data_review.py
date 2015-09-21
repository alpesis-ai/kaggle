#---------------------------------------------------------#
# Project: ASUS - Weibull Train (eta, beta, corr)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printIssues(data, unitList):
    for item in unitList:
        print data[data['unit'] == item]

def test():
    repairPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-repairTrain.csv"
    repair = loadData(repairPath)

    onePoint = ['M9P23', 'M1P10', 'M2P14', 'M6P11', 'M2P07', \
                'M2P08', 'M3P18', 'M3P10', 'M3P23', 'M2P29', \
                'M1P25', 'M3P27']

    twoPoints = ['M8P27', 'M8P10', 'M3P01', 'M6P27', 'M1P27', 'M4P27']

    noRepair = ['M7P23', 'M4P14', 'M6P29', 'M5P29', 'M1P07', \
                'M1P03', 'M1P01', 'M1P08', 'M5P03', 'M8P03', \
                'M5P07', 'M3P29', 'M9P29', 'M7P29', 'M8P07', \
                'M4P07', 'M4P03', 'M4P08', 'M1P14', 'M1P18', \
                'M5P18', 'M5P14', 'M7P07', 'M7P08', 'M0P31', \
                'M0P30', 'M7P14', 'M9P08', 'M4P18', 'M8P23', \
                'M9P07', 'M9P03', 'M2P18', 'M7P18', 'M0P22', \
                'M0P23', 'M0P20', 'M0P21', 'M0P26', 'M0P27', \
                'M0P24', 'M0P25', 'M0P28', 'M0P29', 'M3P08', \
                'M3P07', 'M9P18', 'M6P18', 'M6P14', 'M2P03', \
                'M5P25', 'M0P19', 'M0P18', 'M0P17', 'M0P16', \
                'M0P15', 'M0P14', 'M0P13', 'M0P12', 'M0P11', \
                'M0P10', 'M9P14', 'M3P14', 'M6P08', 'M6P07', \
                'M0P08', 'M0P09', 'M0P01', 'M0P02', 'M0P03', \
                'M0P04', 'M0P05', 'M0P06', 'M0P07', 'M5P08', \
                'M4P29', 'M8P14', 'M8P18', 'M2P23', 'M8P08', \
                'M6P23', 'M1P29', 'M5P23', 'M1P23', 'M8P29', \
                'M4P23']


    printIssues(repair, noRepair)



test()
