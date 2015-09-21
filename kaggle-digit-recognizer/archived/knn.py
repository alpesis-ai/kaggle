'''
------------------------------------------------------
Kaggle: Digit Recognizer
# Model: classification - kNN
# Author: Kelly Chan
# Date: Feb 7 2014
------------------------------------------------------
'''

from numpy import *
import operator

# dataLoad
# extracting dataMatrix from dataFile
def dataLoad(dataFile, delim='\t'):
    label = []
    data = []
    rawData = open(dataFile)
    for line in rawData.readlines():
        thisLine = line.strip().split(delim)
        thisLine = map(int, thisLine)
        thisLabel = thisLine[0]
        thisPixels = thisLine[1:]
        label.append(thisLabel)
        data.append(thisPixels)
    return label, mat(data)

# dataPunch
# (0,255) -> (0,1)
# repunching the data from (1,255) to 1
def dataPunch(dataMatrix):
    rows = shape(dataMatrix)[0]
    cols = shape(dataMatrix)[1]

    for row in range(rows):
        for col in range(cols):
            if int(dataMatrix[row, col]) > 0:
                dataMatrix[row, col] = 1  
    return dataMatrix


# imgPrint
# printing the img of one digit
def imgPrint(imgXVector):
    pixels = shape(imgXVector)[1]
    for row in range(28):
        for col in range(28):
            if (int(imgXVector[0, row*28+col]) > 0):
                print "1",
            else:
                print "0",
        print "\n"

# (classification) kNN
# return the nearest label in k neighbors by computing Euclidean Distance
def knn(testX, trainData, labels, k):
    
    # (testX, trainData) computing Euclidean Distance
    n = trainData.shape[0]
    distanceMatrix = tile(testX, (n,1)) - trainData  # tile: [testX]_n
    distanceMatrix = array(distanceMatrix)**2
    distances = distanceMatrix.sum(axis=1) # axis=0: by cols | aisx=1: by rows
    distances = array(distances)**0.5
    distancesIndex = distances.argsort()  # argsort(): index by ascending values


    # (k, labels) return the nearest label in k neighbors
    kDistances = {}
    for i in range(k):
        label = labels[distancesIndex[i]]
        # counting # of label in k values, .get(key, value), default = 0
        kDistances[label] = kDistances.get(label,0) + 1
    # .iteritems: loop keys, operator.itemgetter(1): sort by values, descending
    kDistances = sorted(kDistances.iteritems(), key=operator.itemgetter(1), reverse = True)
    return kDistances[0][0]

# knnValidate
# testing knn by validation data (extracting from trainData)
def knnValidate(trainData):

    labels, dataMatrix = dataLoad(trainData)
    dataMatrix = dataPunch(dataMatrix)

    N = dataMatrix.shape[0]
    error = 0.0
    splitRatio = 0.10
    validN = int(N * splitRatio)

    for i in range(validN):
        output = knn(dataMatrix[i,:], dataMatrix[validN:N, :], labels[validN:N], 10)
        #print "output: %d, the correct answer: %d" % (output, labels[i]) 

        if (output != labels[i]): 
            error += 1.0
            print "row: %d, output: %d, the correct answer: %d" % (i, output, labels[i]) 
    print "the total error rate: %f" % (error/float(validN))


# digitRecognizer
# classifying testData by knn
def digitRecognizer(trainData, testData, outFile):

    # extracting labels, trainMatrix from train data
    labels, trainMatrix = dataLoad(trainData)
    trainMatrix = dataPunch(trainMatrix)

    # extracting testMatrix from testData
    test = []
    rawTestData = open(testData)
    for line in rawTestData.readlines():
        thisLine = line.strip().split('\t')
        thisLine = map(int, thisLine)
        test.append(thisLine)
    testMatrix = mat(test)
    testMatrix = dataPunch(testMatrix)


    # return test digits by knn algorithm
    error = 0.0
    testN = shape(testMatrix)[0]

    outTxt = open(outFile,'w')
    for i in range(testN):
        output = knn(testMatrix[i], trainMatrix, labels, 10)
        #print "row: %d, output: %d" % (i,output)
        outTxt.write("%d\n" % (output))
    outTxt.close()
        


#trainData = "G:\\vimFiles\\python\\kaggle\\digit_recognizer\\data\\small_train.txt"
#testData = "G:\\vimFiles\\python\\kaggle\\digit_recognizer\\data\\small_test.txt"
#outFile = "G:\\vimFiles\\python\\kaggle\\digit_recognizer\\src\\output\\testOut.txt"

#label, data = dataLoad(trainData, delim='\t')
#print 'label:\n',label
#print data[0]

#dataMatrix = mat(data)
#dataMatrix = dataPunch(dataMatrix)
#print dataMatrix[3]

#imgPrint(dataMatrix[3])

#knn(dataMatrix[0], dataMatrix, label,10)
#knnValidate(dataFile)


trainData = "G:\\vimFiles\\python\\kaggle\\digit_recognizer\\data\\train.txt"
testData = "G:\\vimFiles\\python\\kaggle\\digit_recognizer\\data\\test.txt"
outFile = "G:\\vimFiles\\python\\kaggle\\digit_recognizer\\src\\output\\testOut.txt"
#knnValidate(trainData)
digitRecognizer(trainData, testData, outFile)
