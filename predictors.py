"""
Author: Kelly Chan
Date: June 30 2014

Project: the Predictors of Kaggle Projects

"""

rawPath = "G:/vimFiles/python/kaggle/201406-cpu/data/"
dataPath = "G:/vimFiles/python/kaggle/201406-cpu/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201406-cpu/src/outputs/results/"

import pandas as pd

from sklearn import decomposition
from sklearn import preprocessing

from sklearn import grid_search
from sklearn import cross_validation as cv
from sklearn.cross_validation import StratifiedKFold

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsRegressor

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostClassifier

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

def decomPCA(train, test):
    pca = decomposition.PCA(n_components=12, whiten=True)
    train = pca.fit_transform(train)
    test = pca.transform(test)
    return train, test

def normalize(train, test):
    norm = preprocessing.Normalizer()
    train = norm.fit_transform(train)
    test = norm.transform(test)
    return train, test

def createSVM():
    clf = SVC()
    return clf

def createKNN():
    clf = KNeighborsRegressor(n_neighbors=13,algorithm='kd_tree',weights='uniform',p=1)
    return clf

def createDecisionTree():
    clf = DecisionTreeRegressor(max_depth=None, min_samples_split=1, random_state=0)
    return clf

def createRandomForest():
    clf = RandomForestRegressor(n_estimators=10)
    return clf

def createExtraTree():
    clf = ExtraTreesRegressor(n_estimators=50)
    return clf

def createAdaBoost():
    dt = DecisionTreeClassifier(max_depth=None, min_samples_split=1, random_state=0)
    clf = AdaBoostClassifier(dt, n_estimators=300)
    return clf

def classify(clf, train, features, target, test, filePath):

    clf.fit(train[features], train[target])

    with open(filePath, "wb") as outfile:
        outfile.write("Id,Prediction\n")
        for index, value in enumerate(list(clf.predict(test[features]))):
            outfile.write("%s,%s\n" % (test['Id'].loc[index], value))

def classifyKFold(clf, train, features, target, test, filePath):

    c_range = 10.0 ** np.arange(6.5,7.5,.25)
    gamma_range = 10.0 ** np.arange(-1.5,0.5,.25)
    params = [{'kernel': ['rbf'], 'gamma': gamma_range, 'C': c_range}]

    cvk = cv.StratifiedKFold(train[target], k=5)

    kclf = grid_search.GridSearchCV(clf, param_grid=params, cv=cvk)

    kclf.fit(train[features], train[target])

    with open(filePath, "wb") as outfile:
        outfile.write("Id,Solution\n")
        for index, value in enumerate(list(kclf.predict(test[features]))):
            outfile.write("%s,%s\n" % (test['Id'].loc[index], value))


def chooseAlgorithms(algo, train, features, target, test):

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
        train, test = normalize(train[features], test[features])
        classify(clf, train, features, target, test, outPath+"submission-knn.csv")

def main():
    train = loadData(rawPath + "train.csv")
    test = loadData(rawPath + "test.csv")

    train = splitSampleTime(train)
    train = mapID(train)

    test = splitSampleTime(test)
    test = mapID(test)

    algo = 3
    target = 'cpu_01_busy'
    features = [col for col in train.columns if col not in ['cpu_01_busy', 'sample_time']] 
    chooseAlgorithms(algo, train, features, target, test)

if __name__ == '__main__':
    main()
