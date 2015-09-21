"""
Project: Forest Cover Type Prediction 
- description: http://www.kaggle.com/c/forest-cover-type-prediction
- data: http://www.kaggle.com/c/forest-cover-type-prediction/data

Author: Kelly Chan
Date: May 28 2014

Topic: Exploratory Data Analysis - plot
"""

dataPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/data/"
picsPath = "G:/vimFiles/python/kaggle/201405-Forest/src/outputs/pics/"

import pandas as pd
from ggplot import *

def loadData(datafile):
    return pd.read_csv(datafile)

def plotHist(data, x):
    p = ggplot(aes(x=x), data=data)
    p = p + geom_histogram()
    p = p + ggtitle("Histogram - %s" % (str(x)))
    ggsave(p, "%stemp/Histogram-%s.png" % (picsPath, str(x)))

def plotPoints(data, x, y):
    p = ggplot(aes(x=x, y=y), data=data)
    p = p + geom_point()
    p = p + ggtitle("Scatter - %s vs. %s" % (str(x), str(y)))
    ggsave(p, "%stemp/Scatter-%s_vs_%s.png" % (picsPath, str(x), str(y)))

def main():
    train = loadData(dataPath + "train.csv")
    
    cols = [col for col in train.columns if col not in ['Id']] 
    for col in cols:
        plotHist(train, col)

    xCol = 'Cover_Type'
    yCols = [col for col in train.columns if col not in ['Id', 'Cover_Type']] 
    for yCol in yCols:
        plotPoints(train, xCol, yCol)


if __name__ == '__main__':
    main()
