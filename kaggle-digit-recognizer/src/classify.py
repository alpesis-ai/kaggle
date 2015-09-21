"""
Project: Digit Recognizer 
Author: Kelly Chan
Date: June 4 2014
"""

rawPath = "G:/vimFiles/python/kaggle/201406-digitRecognizer/data/"
dataPath = "G:/vimFiles/python/kaggle/201406-digitRecognizer/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201406-digitRecognizer/src/outputs/results/"

import pandas as pd

from sklearn import decomposition

from sklearn.svm import SVC

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier

def loadData(datafile):
    return pd.read_csv(datafile)

def decomPCA(train, test):
    pca = decomposition.PCA(n_components=256, whiten=True)
    train = pca.fit_transform(train)
    test = pca.transform(test)
    return train, test

def createSVM():
    clf = SVC()
    return clf

def createKNN():
    clf = KNeighborsClassifier(n_neighbors=13,algorithm='kd_tree',weights='uniform',p=1)
    return clf

def createDecisionTree():
    clf = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createRandomForest():
    clf = RandomForestClassifier(n_estimators=500, max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createExtraTree():
    clf = ExtraTreesClassifier(n_estimators=100, max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createAdaBoost():
    dt = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
    clf = AdaBoostClassifier(dt, n_estimators=300)
    return clf

def classify(clf, train, cols, target, test, filePath):
    clf.fit(train[cols], train[target])

    with open(filePath, "wb") as outfile:
        outfile.write("ImageId,Label\n")
        for index, value in enumerate(list(clf.predict(test[cols]))):
            outfile.write("%s,%s\n" % (index+1, value))

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

        clf = createSVM()
        classify(clf, train, features, target, test, outPath+"submission-svm.csv")

        clf = createKNN()
        classify(clf, train, features, target, test, outPath+"submission-knn.csv")

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

    elif algo == 5:
        clf = createSVM()
        classify(clf, train, features, target, test, outPath+"submission-svm.csv")

    elif algo == 6:
        clf = createKNN()
        classify(clf, train, features, target, test, outPath+"submission-knn.csv")

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
    - 5: svm
    - 6: knn
    """
    dataset = 2
    algo = 6

    train, test = chooseDataset(dataset)

    target = 'label'
    features = [col for col in train.columns if col not in ['label']]

    #train, test = decomPCA(train[features], test[features])
    chooseAlgorithms(algo, train, test, target, features)



if __name__ == '__main__':
    main()
