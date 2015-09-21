"""
Project: Titanic: Machine Learning from Disaster
Author: Kelly Chan
Date: June 4 2014
"""

rawPath = "G:/vimFiles/python/kaggle/201406-titanic/data/"
dataPath = "G:/vimFiles/python/kaggle/201406-titanic/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201406-titanic/src/outputs/results/"

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier

def loadData(datafile):
    return pd.read_csv(datafile)

def createFamilySize(data):
    data['FamilySize'] = data['SibSp'] + data['Parch'] + 1
    return data

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
        outfile.write("PassengerId,Survived\n")
        for index, value in enumerate(list(clf.predict(test[cols]))):
            outfile.write("%s,%s\n" % (test['PassengerId'].loc[index], value))

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
    dataset = 2
    algo = 2

    train, test = chooseDataset(dataset)

    train = createFamilySize(train)
    test = createFamilySize(test)

    target = 'Survived'
    features = [col for col in train.columns if col not in ['PassengerId', \
        'Survived', 'Name', 'Ticket', 'Cabin', 'unnamed']]

    chooseAlgorithms(algo, train, test, target, features)



if __name__ == '__main__':
    main()
