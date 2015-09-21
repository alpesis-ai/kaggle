import pandas
import numpy as np
import matplotlib.pyplot as plt
from ggplot import *


def dataLoad(datafile):
    rawData = pandas.read_csv(datafile)
    rawData['repairDate'] = pandas.to_datetime(rawData['repairDate'])
    rawData['saleDate'] = pandas.to_datetime(rawData['saleDate'])
    return rawData

def repairCount(data, colNames):
    return data.groupby(colNames).sum()


def factorBarPlot(data, feature):
    p = ggplot(data, aes(feature)) 
    p = p + geom_bar()
    p = p + ggtitle("Bar Plot") + labs(feature)
    return p

def numHistPlot(data, feature):
    p = ggplot(data, aes(x=feature)) 
    p = p + geom_histogram()
    p = p + ggtitle("Histogram") + labs(feature,"Freq")
    return p


def tsYearPlot(data, targetDate, targetFeature):
    # set_index
    targetData = data.set_index([targetDate])

    # reshaping data
    targetDataByYear = targetData.groupby(targetData.index.year).sum()
    targetDataByYear.index.name = 'year'
    targetDataByYear = targetDataByYear.reset_index()

    # plotting
    p = ggplot(targetDataByYear, aes('year', weight=targetFeature)) 
    p = p + geom_bar()
    p = p + ggtitle('Yearly Review')

    return p


def tsMonthPlot(data, targetDate, targetFeature):
    # set_index
    targetData = data.set_index([targetDate])

    # reshaping data
    targetDataByYear = targetData.groupby(targetData.index.month).sum()
    targetDataByYear.index.name = 'month'
    targetDataByYear = targetDataByYear.reset_index()

    # plotting
    p = ggplot(targetDataByYear, aes('month', weight=targetFeature)) 
    p = p + geom_bar()
    p = p + ggtitle('Monthly Review')

    return p

def tsRepairPlot(data, date, factorFeature, numFeature):
    newData = data.loc[:, [date, factorFeature, numFeature]]
    newData = newData.reset_index(date)

    p = ggplot(aes(x = date, y = numFeature, colour = factorFeature), data =newData)
    p = p + geom_point()
    p = p + ggtitle("Months to be repaired after saleDate - by " + factorFeature)

    return p

def saveTSRepairPlot(dataPath, data, feature, date, factorFeature, numFeature):
    for item in set(feature):
        p = tsRepairPlot(data[feature == item], date, factorFeature, numFeature)
        ggsave(p, dataPath + numFeature + "_by_" + date + "-" + item + ".png") 


repairTrain = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-small-repairTrain.csv"
#repairTrain = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-repairTrain.csv"

repairTrain = dataLoad(repairTrain)

#print repairCount(repairTrain, ['module','component', 'betweenMonths'])
#print repairCount(repairTrain, ['unit', 'repairDate', 'saleDate','betweenMonths'])
#print repairMonths(repairTrain['saleDate'], repairTrain['repairDate'])
#histPlot(repairTrain['numRepair'])


#print factorBarPlot(repairTrain, 'factor(module)')
#print factorBarPlot(repairTrain, 'factor(component)')
#print factorBarPlot(repairTrain, 'factor(unit)')

#print numHistPlot(repairTrain, 'betweenmonths')
#print numHistPlot(repairTrain, 'numRepair')

#print tsYearPlot(repairTrain[repairTrain['module'] == 'M1'], 'repairDate', 'numRepair')
#print tsMonthPlot(repairTrain[repairTrain['module'] == 'M1'], 'repairDate', 'numRepair')



#odulePath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\pics\\betweenMonths_by_saleDate-by_module\\"
#componentPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\pics\\betweenMonths_by_saleDate-by_component\\"
#unitPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\outputs\\pics\\betweenMonths_by_saleDate-by_unit\\"

#saveTSRepairPlot(modulePath, \
#                 repairTrain, repairTrain['module'], \
#                 'saleDate', 'module', 'betweenMonths')

#saveTSRepairPlot(componentPath, \
#                 repairTrain, repairTrain['component'], \
#                 'saleDate', 'component', 'betweenMonths')


#saveTSRepairPlot(unitPath, \
#                 repairTrain, repairTrain['unit'], \
#                 'saleDate', 'unit', 'betweenMonths')


