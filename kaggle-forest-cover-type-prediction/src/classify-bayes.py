"""
Project: Forest Cover Type Prediction 
- description: http://www.kaggle.com/c/forest-cover-type-prediction
- data: http://www.kaggle.com/c/forest-cover-type-prediction/data

Author: Kelly Chan
Date: May 28 2014

Topic: Classification - Random Forest
"""

dataPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/results/"

import pandas as pd
from sklearn.naive_bayes import GaussianNB

def loadData(datafile):
    return pd.read_csv(datafile)

def classifyRF(test, train, cols, target):
    clf = GaussianNB()
    clf.fit(train[cols], train[target])

    with open(outPath+"submission-gnb.csv", "wb") as outfile:
        outfile.write("Id,Cover_Type\n")
        for index, value in enumerate(list(clf.predict(test[cols]))):
            outfile.write("%s,%s\n" % (test['Id'].loc[index], value))

def main():

    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    target = 'Cover_Type'
    features = [col for col in train.columns if col not in ['Id', 'Cover_Type', 'Unnamed']]
    submission = classifyRF(test, train, features, target)


if __name__ == '__main__':
    main()


