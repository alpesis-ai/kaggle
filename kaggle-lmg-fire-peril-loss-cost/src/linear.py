"""
Project: Liberty Mutual Group - Fire Peril Loss Cost

Author: Kelly Chan
Date: Sept 2 2014
"""

import numpy as np
import pandas as pd

from sklearn.linear_model import Ridge, Lasso

def loadData(datafile):
    return pd.read_csv(datafile)

def setRidge():
    clf = Ridge()
    return clf

def predict(clf, tr, ts):
    clf.fit(tr, train['target'].values)
    return clf.predict(ts)

def outCSV(samples, preds, outPath):
    samples['target'] = preds
    sample.to_csv(outPath+'submission.csv', index=False)


def main():

    dataPath = "G:/vimFiles/python/kaggle/201408-LMGfire/data/"
    outPath = "G:/vimFiles/python/kaggle/201408-LMGfire/src/outputs/results/"
    
    train = loadData(dataPath+"train.csv")
    test = loadData(dataPath+"test.csv")
    samples = loadData(dataPath+"sampleSubmission.csv")

    tr = train[['var11', 'var12', 'var13', 'var14', 'var15', 'var16', 'var17']]
    ts = test[['var11', 'var12', 'var13', 'var14', 'var15', 'var16', 'var17']]
    tr = np.nan_to_num(np.array(tr))
    ts = np.nan_to_num(np.array(ts))

    clf = setRidge()
    preds = predict(clf, tr, ts)
    outCSV(samples, preds, outPath)


if __name__ == '__main__':
    main()



