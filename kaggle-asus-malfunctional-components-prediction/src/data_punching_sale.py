#---------------------------------------------------------#
# Project: ASUS - data punching (sale)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import csv
from datetime import datetime

def dataLoad(datafile):

    data = []
    with open(datafile, 'r') as rawData:
        for line in rawData.readlines():
            thisLine = []
            module, component, saleDate, numSale = line.strip().split(',')
            unit = module + component

            startDate = datetime.strptime(saleDate, '%Y/%m')
            endDate = datetime.strptime('2008/12', '%Y/%m')
            betweenMonths = (endDate.year * 12 - (12 - endDate.month)) - (startDate.year * 12 - (12 - startDate.month))
            betweenMonths = betweenMonths + 1 # included start/end month

            thisLine = [module, component, unit, saleDate, numSale, betweenMonths]
            data.append(thisLine)
    return data


def punching(data, outfile):
    header = ['module', 'component', 'unit', 'saleDate', 'numSale', 'betweenMonths']
    with open(outfile, 'wb') as csvfile:
        cleanData = csv.writer(csvfile, delimiter=',')
        cleanData.writerow(header)
        for line in data:
            cleanData.writerow(line)

def main(rawData, outfile):
    data = dataLoad(rawData)
    punching(data, outfile)


saleTrain = "G:\\vimFiles\\python\\kaggle\\ASUS\\data\\SaleTrain.txt"
outfile = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-saleTrain.csv"

if __name__ == "__main__":
    main(saleTrain, outfile)
