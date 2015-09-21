'''
----------------------------------------------------------------
Kaggle: PAKDD 2014 - ASUS Malfunctional Components Prediction

# Author: Kelly Chan
# Date: Feb 11 2014
----------------------------------------------------------------
'''

def dataRepairLoad(dataPath, delim):

    module = []
    component = []
    moduleComponent = []

    saleDate = []
    saleYear = []
    saleMonth = []

    repairDate = []
    repairYear = []
    repairMonth = []

    repairNum = []

    rawData = open(dataPath)
    for line in rawData.readlines():
        thisModule, thisComponent, thisSaleDate, thisRepairDate, thisRepairNum = line.strip().split(delim)
        thisModuleComponent = thisModule + thisComponent
        thisSaleYear, thisSaleMonth = thisSaleDate.split('/')
        thisSaleYear = int(thisSaleYear)
        thisSaleMonth = int(thisSaleMonth)
        thisRepairYear, thisRepairMonth = thisRepairDate.split('/')
        thisRepairYear = int(thisRepairYear)
        thisRepairMonth = int(thisRepairMonth)
        thisRepairNum = int(thisRepairNum)

        module.append(thisModule)
        component.append(thisComponent)
        moduleComponent.append(thisModuleComponent)

        saleDate.append(thisSaleDate)
        saleYear.append(thisSaleYear)
        saleMonth.append(thisSaleMonth)

        repairDate.append(thisRepairDate)
        repairYear.append(thisRepairYear)
        repairMonth.append(thisRepairMonth)

        repairNum.append(thisRepairNum)

    return moduleComponent, module, component, \
           saleDate, saleYear, saleMonth, \
           repairDate, repairYear, repairMonth, \
           repairNum


def createComponentSet(module, component, moduleSet):

    componentSet = []

    for i in range(len(module)):
        if (module[i] == moduleSet):
            print component[i]
            

dataPath = "G:\\vimFiles\\python\\kaggle\\ASUS\\data\\RepairTrain.txt"
moduleComponent, module, component, saleDate, saleYear, saleMonth, repairDate, repairYear, repairMonth, repairNum = dataRepairLoad(dataPath, ',')


#print len(module)
#print set(module)
#print set(component)
#print set(moduleComponent)
#print len(set(moduleComponent))


#print set(saleDate)
#print len(set(saleDate))
#print set(saleYear)
#print set(saleMonth)

#print set(repairDate)
#print len(set(repairDate))
#print set(repairYear)
#print set(repairMonth)
#print set(repairNum)


print createComponentSet(module, component, 'M1')
