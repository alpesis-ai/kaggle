"""
Project: Forest Cover Type Prediction 
- description: http://www.kaggle.com/c/forest-cover-type-prediction
- data: http://www.kaggle.com/c/forest-cover-type-prediction/data

Author: Kelly Chan
Date: May 30 2014

Topic: Classifications - master
"""

"""
Function Tree

- chooseDataset
     |------ loadData

- chooseAlgorithms
     |------ createDecisionTree
     |------ createRandomForest
     |------ createExtraTree
     |------ createAdaBoost

"""

rawPath = "G:/vimFiles/python/kaggle/201405-Forest/data/"
dataPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/results/"

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier

def loadData(datafile):
    return pd.read_csv(datafile)


def createDecisionTree():
    clf = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createRandomForest():
    clf = RandomForestClassifier(n_estimators=500, max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createExtraTree():
    clf = ExtraTreesClassifier(n_estimators=500, max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createAdaBoost():
    dt = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
    clf = AdaBoostClassifier(dt, n_estimators=300)
    return clf

def classify(clf, train, cols, target, test, filePath):
    clf.fit(train[cols], train[target])

    with open(filePath, "wb") as outfile:
        outfile.write("Id,Cover_Type\n")
        for index, value in enumerate(list(clf.predict(test[cols]))):
            outfile.write("%s,%s\n" % (test['Id'].loc[index], value))


def chooseDataset(dataset):
    if dataset == 1:
        train = loadData(rawPath + "train.csv")
        test = loadData(rawPath + "test.csv")
    elif dataset == 2:
        train = loadData(dataPath + "train.csv")
        test = loadData(dataPath + "test.csv")
    return train, test

def chooseAlgorithms(algo, train, test, target, features):

    if algo == 0:

        clf = createDecisionTree()
        classify(clf, train, features, target, test, outPath+"submission-decisiontree.csv")        

        clf = createRandomForest()
        classify(clf, train, features, target, test, outPath+"submission-randomforest.csv")

        clf = createExtraTree()
        classify(clf, train, features, target, test, outPath+"submission-extratree.csv")

        clf = createAdaBoost()
        classify(clf, train, features, target, test, outPath+"submission-adaboost.csv")

    elif algo == 1:
        clf = createDecisionTree()
        classify(clf, train, features, target, test, outPath+"submission-decisiontree.csv")

    elif algo == 2:
        clf = createRandomForest()
        classify(clf, train, features, target, test, outPath+"submission-randomforest.csv")
    
    elif algo == 3:
        clf = createExtraTree()
        classify(clf, train, features, target, test, outPath+"submission-extratree.csv")

    elif algo == 4:
        clf = createAdaBoost()
        classify(clf, train, features, target, test, outPath+"submission-adaboost.csv")


def main():

    """ selections: dataset and algorithms

    dataset:
    - 1: raw data - Wilderness_Area, Soil_Type are binary codes
    - 2: punched data - Wilderness_Area, Soil_Type are combined

    algo: algorithms
    - 0: all
    - 1: decision tree
    - 2: random forest
    - 3: extra tree
    - 4: adaboost
    """
    dataset = 1
    algo = 1

    train, test = chooseDataset(dataset)

    target = 'Cover_Type'
    features = [col for col in train.columns if col not in ['Id', 'Cover_Type', 'Unnamed']]

    chooseAlgorithms(algo, train, test, target, features)



if __name__ == '__main__':
    main()


