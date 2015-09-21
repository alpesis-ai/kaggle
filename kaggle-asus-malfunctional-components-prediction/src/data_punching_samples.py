#---------------------------------------------------------#
# Project: ASUS - data punching (samples)
# Author: Kelly Chan
# Date: Mar 20 2014
#---------------------------------------------------------#

import csv

def dataLoad(datafile):

    data = []
    index = 1
    with open(datafile, 'r') as rawData:
        for line in rawData.readlines():
            thisLine = []
            module, component, year, month = line.strip().split(',')

            unit = module + component
            predDate = year + "/" + month

            numPred = 0

            thisLine = [index, module, component, unit, predDate, numPred]
            data.append(thisLine)
            index += 1

    return data

def punching(data, outfile):
    header = ['id', 'module', 'component', 'unit', 'predDate', 'numPred']
    with open(outfile, 'wb') as csvfile:
        cleanData = csv.writer(csvfile, delimiter=',')
        cleanData.writerow(header)
        for line in data:
            cleanData.writerow(line)

def main(rawData, outfile):
    data = dataLoad(rawData)
    punching(data, outfile)


samples = "G:\\vimFiles\\python\\kaggle\\ASUS\\data\\Output_TargetID_Mapping.txt"
outfile = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-samples.csv"

if __name__ == "__main__":
    main(samples, outfile)



