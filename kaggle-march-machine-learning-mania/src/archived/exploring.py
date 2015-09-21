#---------------------------------------------#
# Project: March Machine Learning Mania
# Author: Kelly Chan
# Date: Mar 11 2014
#---------------------------------------------#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *


def dataLoad(datafile):
    data = pd.read_csv(datafile)
    return data

def numHistPlot(data, feature):
    p = ggplot(data, aes(x=feature)) 
    p = p + geom_histogram()
    p = p + ggtitle("Histogram") + labs(feature,"Freq")
    return p

regular = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\regular_season_results.csv"
tourney = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_results.csv"

preRegular = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_predicted.csv"
evalRegular = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_predicted_eval.csv"
regularScores = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_scores.csv"

regular = dataLoad(regular)
tourney = dataLoad(tourney)
preRegular = dataLoad(preRegular)
evalRegular = dataLoad(evalRegular)
regularScores = dataLoad(regularScores)


regular['diff'] = regular['wscore'] - regular['lscore']
#print regular
#print numHistPlot(regular, 'diff')

#print preRegular.head(10)

plotData = preRegular[preRegular['numGames'] > 0]
#print numHistPlot(plotData, 'numGames')

left = pd.DataFrame({'key': preRegular['idName'], 'preWinProb': preRegular['winProb']})
right = pd.DataFrame({'key': evalRegular['idName'], 'realWinProb': evalRegular['winProb']})

evalData = pd.merge(left, right, on='key')
evalData['diff'] = evalData['realWinProb'] - evalData['preWinProb']
evalData = evalData[evalData['realWinProb'] >= 0]
evalData = evalData[evalData['preWinProb'] >= 0]
#print evalData
print len(evalData[evalData['diff'] == 0].index)
print len(evalData[evalData['diff'] > 0].index)
print len(evalData[evalData['diff'] < 0].index)
#print numHistPlot(evalData, 'diff')

regularScores = regularScores[regularScores['numGames'] > 0]
#print regularScores[regularScores['scoreRate'] == 0]
#print numHistPlot(regularScores, 'scoreRate')

print ggplot(regularScores, aes('scoreRate', 'winProb')) + geom_point() 
