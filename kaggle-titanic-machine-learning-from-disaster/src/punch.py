"""
Project: Titanic: Machine Learning from Disaster
Author: Kelly Chan
Date: June 4 2014
"""

rawPath = "G:/vimFiles/python/kaggle/201406-titanic/data/"
dataPath = "G:/vimFiles/python/kaggle/201406-titanic/src/outputs/data/"

import pandas as pd

def loadData(datafile):
    return pd.read_csv(datafile)

def fillAge(data):
    meanAge = data['Age'].mean()
    data['Age'] = data['Age'].fillna(meanAge)
    return data

def fillFare(data):
    meanFare = data['Fare'].mean()
    data['Fare'] = data['Fare'].fillna(meanFare)
    return data

def mapSex(data):
    coded = {'male': 1, 'female': 2}
    data['Sex'] = data['Sex'].astype(str).map(coded)
    return data

def mapEmbarked(data):
    coded = {'C': 1, 'Q': 2, 'S': 3}
    data['Embarked'] = data['Embarked'].astype(str).map(coded)
    data['Embarked'] = data['Embarked'].fillna(4)
    return data

def main():
    train = loadData(rawPath + "train.csv")
    test = loadData(rawPath + "test.csv")

    train = fillAge(train)
    train = fillFare(train)
    train = mapSex(train)
    train = mapEmbarked(train)
    train.to_csv(dataPath + "train.csv")

    test = fillAge(test)
    test = fillFare(test)
    test = mapSex(test)
    test = mapEmbarked(test)
    test.to_csv(dataPath + "test.csv")


if __name__ == '__main__':
    main()
