"""
Project: Burn CPU Burn
Author: Kelly Chan
Date: June 6 2014
"""

rawPath = "G:/vimFiles/python/kaggle/201406-cpu/data/"
dataPath = "G:/vimFiles/python/kaggle/201406-cpu/src/outputs/data/"

import pandas as pd

from sklearn import preprocessing


def loadData(datafile):
    return pd.read_csv(datafile)

def splitSampleTime(data):

    sub = pd.DataFrame(data.sample_time.str.split(' ').tolist(), columns="date time".split())
    date = pd.DataFrame(sub.date.str.split('-').tolist(), columns="year month day".split())
    time = pd.DataFrame(sub.time.str.split(':').tolist(), columns="hour minute second".split())
    
    data['year'] = date['year']
    data['month'] = date['month']
    data['day'] = date['day']

    data['hour'] = time['hour']
    data['minute'] = time['minute']

    return data

def mapID(data):
    coded = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7}
    data['m_id'] = data['m_id'].astype(str).map(coded)
    return data

def normalize(train, test):
    norm = preprocessing.Normalizer()
    train = norm.fit_transform(train)
    test = norm.transform(test)
    return train, test

def main():
    train = loadData(rawPath + "train.csv")
    test = loadData(rawPath + "test.csv")

    train = splitSampleTime(train)
    train = mapID(train)

    test = splitSampleTime(test)
    test = mapID(test)


    features = [col for col in train.columns if col not in ['cpu_01_busy', 'sample_time']]

    train, test = normalize(train[features], test[features])
    train.to_csv(dataPath + "train.csv")
    test.to_csv(dataPath + "test.csv")

    #features = [col for col in train.columns if col not in ['cpu_01_busy', 'sample_time']]
    #deTrain, deTest = decomPCA(train[features], test[features])
    #deTrain.to_csv(dataPath + "train.csv")
    #deTest.to_csv(dataPath + "test.csv")
    #print train['cpu_01_busy']


if __name__ == '__main__':
    main()
