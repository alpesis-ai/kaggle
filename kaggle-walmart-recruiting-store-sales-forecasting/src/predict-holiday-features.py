"""
Project: Walmart Recruiting - Store Sales Forecasting 
Author: Kelly Chan
Date: June 4 2014
"""

dataPath = "G:/vimFiles/python/kaggle/201406-Walmart/data/"
punchPath = "G:/vimFiles/python/kaggle/201406-Walmart/src/outputs/data/"
outPath = "G:/vimFiles/python/kaggle/201406-Walmart/src/outputs/results/"

import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor

def loadData(datafile):
    return pd.read_csv(datafile)

def splitDate(data):
    date = pd.DataFrame(data.Date.str.split('-').tolist(), columns="year month day".split())
    data['year'] = date['year']
    data['month'] = date['month']
    data['day'] = date['day']
    return data

def combineFeatures(data, features):
    data = pd.merge(data, features, left_on=["Store", "Date", "IsHoliday"], \
                                    right_on=["Store", "Date", "IsHoliday"], \
                                    how="left")

    data = data.fillna(0)
    return data

def createID(data):
    data['Id'] = data['Store'].astype(str) + '_' + \
                 data['Dept'].astype(str) + '_' + \
                 data['Date'].astype(str)
    return data

def createDecisionTree():
    est = DecisionTreeRegressor()
    return est

def createRandomForest():
    est = RandomForestRegressor(n_estimators=10)
    return est

def createExtraTree():
    est = ExtraTreesRegressor(n_estimators=10)
    return est

def predict(est, train, test, features, target):

    est.fit(train[features], train[target])

    with open(outPath + "submission-extratrees.csv", 'wb') as f:
        f.write("Id,Weekly_Sales\n")

        for index, value in enumerate(list(est.predict(test[features]))):
            f.write("%s,%s\n" % (test['Id'].loc[index], int(value)))


def main():

    features = loadData(dataPath + "features.csv")

    train = loadData(dataPath + "train.csv")
    test = loadData(dataPath + "test.csv")

    train = splitDate(train)
    train = combineFeatures(train, features)
    train.to_csv(punchPath + "train.csv")

    test = splitDate(test)
    test = combineFeatures(test, features)
    test.to_csv(punchPath + "test.csv")

    test = createID(test)

    target = 'Weekly_Sales'
    features = [col for col in train.columns if col not in ['Date', \
            'Weekly_Sales', 'Fuel_Price', 'CPI', 'Unemployment']]

    #est = createRandomForest()
    est = createExtraTree()
    predict(est, train, test, features, target)



if __name__ == "__main__":
    main()


