#----------------------------------------------------#
# Project: March Machine Learning Mania 
# Author: Kelly Chan
# Date: Mar 14 2014
#----------------------------------------------------#

import pandas
from numpy import *
from ggplot import *
import csv

def dataLoad(datafile):
    return pandas.read_csv(datafile)

def barPlot(data, feature):
    p = ggplot(aes(x=feature), data)
    p = p + geom_bar()
    return p

def histPlot(data, feature):
    p = ggplot(aes(x=feature), data)
    p = p + geom_histogram()
    return p

def scatterPlot(data, featureX, featureY):
    p = ggplot(aes(x=featureX, y=featureY), data)
    p = p + geom_point()
    return p

def testBarPlot(data):
    for item in data.columns:
        feature = ['factor(', item, ')']
        print barPlot(regular, ''.join(feature))

def testHistPlot(data):
    for item in data.columns[1:6]:
        print histPlot(data, item)

def teamData(data, team):
    wteamData = data[data['wteam'] == team]
    lteamData = data[data['lteam'] == team]
    return wteamData, lteamData



regular = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\regular_season_results.csv"
tourney = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_results.csv"
samples = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\sample_submission.csv"
seeds = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_seeds.csv"
slots = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_slots.csv"
teams = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\teams.csv"

regular = dataLoad(regular)
tourney = dataLoad(tourney)
samples = dataLoad(samples)
seeds = dataLoad(seeds)
slots = dataLoad(slots)
teams = dataLoad(teams)

#daynum	wteam	wscore	lteam	lscore	wloc	numot

#print regular.dtypes

#print barPlot(regular, 'factor(daynum)')
#print histPlot(regular, 'daynum')
#print histPlot(regular, 'wteam')

#testBarPlot(tourney)
#testHistPlot(tourney)
regular['diffScore'] = regular['wscore'] - regular['lscore']
#print scatterPlot(regular, 'numot', 'diffScore')

w511Data, l511Data = teamData(regular, 511)
#print w511Data
#print scatterPlot(w511Data, 'lteam', 'diffScore')
#print barPlot(w511Data, 'season')
w511Data['lteam'] = w511Data['lteam'].astype(str)
print barPlot(w511Data, 'lteam')
#print w511Data[w511Data['lteam'] == 723]
