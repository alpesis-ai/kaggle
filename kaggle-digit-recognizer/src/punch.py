"""
Project: Digit Recognizer 
Author: Kelly Chan
Date: June 4 2014
"""

rawPath = "G:/vimFiles/python/kaggle/201406-digitRecognizer/data/"
dataPath = "G:/vimFiles/python/kaggle/201406-digitRecognizer/src/outputs/data/"

import pandas as pd

def loadData(datafile):
    return pd.read_csv(datafile)

def mapPixels(data):

    pixDict = {}
    for i in range (256):
        if i == 0:
            pixDict[str(i)] = 0
        else:
            pixDict[str(i)] = 1

    features = [col for col in data.columns if col not in ['label']]
    for feature in features:
        data[feature] = data[feature].astype(str).map(pixDict)

    return data

def main():
    train = loadData(rawPath + "train.csv")
    test = loadData(rawPath + "test.csv")

    train = mapPixels(train)
    train.to_csv(dataPath + "train.csv")

    test = mapPixels(test)
    test.to_csv(dataPath + "test.csv")


if __name__ == '__main__':
    main()
