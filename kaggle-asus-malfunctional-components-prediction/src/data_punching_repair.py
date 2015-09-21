import csv
from datetime import datetime

def dataLoad(datafile):

    data = []
    with open(datafile, 'r') as rawData:
        for line in rawData.readlines():
            thisLine = []
            module, component, saleDate, repairDate, numRepair = line.strip().split(',')
            
            # correcting data
            if (module == "M7") and (component == "P06") and \
               (saleDate == "2007/9") and (repairDate == "2007/7") and \
               (numRepair == "1"):
                   saleDate = "2007/7"
                   repairDate = "2007/9"

            unit = module + component

            startDate = datetime.strptime(saleDate, '%Y/%m')
            endDate = datetime.strptime(repairDate, '%Y/%m')
            betweenMonths = (endDate.year * 12 - (12 - endDate.month)) - (startDate.year * 12 - (12 - startDate.month))
            betweenMonths = betweenMonths + 1 # included start/end month

            thisLine = [module, component, unit, saleDate, repairDate,betweenMonths, numRepair]
            data.append(thisLine)
    return data

def punching(data, outfile):
    header = ['module', 'component', 'unit', 'saleDate', 'repairDate', 'betweenMonths', 'numRepair']
    with open(outfile, 'wb') as csvfile:
        cleanData = csv.writer(csvfile, delimiter=',')
        cleanData.writerow(header)
        for line in data:
            cleanData.writerow(line)

def main(rawData, outfile):
    data = dataLoad(rawData)
    punching(data, outfile)


def datasetChoose(x, small_repairTrain, small_outfile, repairTrain, repair_outfile):
    # x = 1: small_repairTrain
    # x = 2: repairTrain
    if (x == 1):
        repairTrain = small_repairTrain
        outfile = small_outfile
    elif (x == 2):
        repairTrain = repairTrain
        outfile = repair_outfile
    return repairTrain, outfile

def main(rawData, outfile):
    data = dataLoad(rawData)
    punching(data, outfile)



small_repairTrain = "G:\\vimFiles\\python\\kaggle\\ASUS\\data\\small-RepairTrain.txt"
small_outfile = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-small-repairTrain.csv"
repairTrain = "G:\\vimFiles\\python\\kaggle\\ASUS\\data\\RepairTrain.txt"
repair_outfile = "G:\\vimFiles\\python\\kaggle\\ASUS\\src\\data\\clean-repairTrain.csv"


if __name__ == "__main__":
    x = 2
    repairTrain, outfile = datasetChoose(x, small_repairTrain, small_outfile, repairTrain, repair_outfile)
    main(repairTrain, outfile)
