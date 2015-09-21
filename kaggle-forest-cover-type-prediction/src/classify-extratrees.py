"""
Project: Forest Cover Type Prediction 
- description: http://www.kaggle.com/c/forest-cover-type-prediction
- data: http://www.kaggle.com/c/forest-cover-type-prediction/data

Author: Kelly Chan
Date: May 30 2014

Topic: Classification - Extra Tree
"""

dataPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/results/"

import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier

def loadData(datafile):
    return pd.read_csv(datafile)

def classifyET(test, train, cols, target):
    clf = ExtraTreesClassifier(n_estimators=500, max_depth=None, min_samples_split=1, random_state=0)
    clf.fit(train[cols], train[target])

    with open(outPath+"submission-extratree.csv", "wb") as outfile:
        outfile.write("Id,Cover_Type\n")
        for index, value in enumerate(list(clf.predict(test[cols]))):
            outfile.write("%s,%s\n" % (test['Id'].loc[index], value))

def main():

    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    target = 'Cover_Type'
    features = [col for col in train.columns if col not in ['Id', 'Cover_Type', 'Unnamed']]
    submission = classifyET(test, train, features, target)


if __name__ == '__main__':
    main()

