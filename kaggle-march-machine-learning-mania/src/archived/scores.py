#---------------------------------------------#
# Project: March Machine Learning Mania
# Author: Kelly Chan
# Date: Mar 11 2014
#---------------------------------------------#

import pandas as pd
from numpy import *
import csv


def dataLoad(datafile):
    data = pd.read_csv(datafile)
    return data


def calProb(data, targetSeason, targetTeam, compareTeam):
    wteamData = data[data.wteam == targetTeam]
    wteamData = wteamData[wteamData.lteam == compareTeam]

    lteamData = data[data.lteam == targetTeam]
    lteamData = lteamData[lteamData.wteam == compareTeam]

    numWins = len(wteamData.index)
    numLoses = len(lteamData.index)
    numGames = numWins + numLoses


    idName = targetSeason + "_" + str(targetTeam) + "_" + str(compareTeam)

    if numGames == 0:
        return [idName, str(numWins), str(numGames), str(-1)]
    else:
        winProb = float(numWins) / float(numGames)
        return [idName, str(numWins), str(numGames), str(winProb)]


def outPredict(outfile, testData, trainData):
    with open(outfile, 'wb') as f:
        outcsv = csv.writer(f, delimiter=',')
        outcsv.writerow(['idName', 'numWins', 'numGames', 'winProb'])

        for item in testData['id']:
            season, targetTeam, compareTeam = item.split('_')
            record = calProb(trainData, str(season), int(targetTeam), int(compareTeam))

            outcsv.writerow(record)



regular = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\regular_season_results.csv"
tourney = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_results.csv"
samples = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\sample_submission.csv"

outRegular = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_predicted.csv"
outTourney = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\tourney_predicted.csv"

outRegularEval = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_predicted_eval.csv"

regular = dataLoad(regular)
tourney = dataLoad(tourney)
samples = dataLoad(samples)

#regularTrain = regular.iloc[:59531, :]
#regularEval = regular.iloc[59531:, :]
#tourney = tourney.iloc[:828, :]

#outPredict(outRegular, samples, regularTrain)
#outPredict(outRegularEval, samples, regularEval)
#outPredict(outTourney, samples, tourney)

def sigmoid(z):
    return 1.0/(1+exp(-z))

def diffScores(data, targetSeason, targetTeam, compareTeam):
    wteamData = data[data.wteam == targetTeam]
    wteamData = wteamData[wteamData.lteam == compareTeam]

    lteamData = data[data.lteam == targetTeam]
    lteamData = lteamData[lteamData.wteam == compareTeam]

    wteamData['diffWin'] = wteamData['wscore'] -  wteamData['lscore']
    lteamData['diffLose'] = lteamData['lscore'] - lteamData['wscore']

    totalWScore = wteamData['diffWin'].sum()
    totalLScore = lteamData['diffLose'].sum()
    diffScore = totalWScore + totalLScore

    numWins = len(wteamData.index)
    numLoses = len(lteamData.index)
    numGames = numWins + numLoses

    if numGames == 0:
        scoreRate = 0
        winProb = 0.5
    else:
        scoreRate = float(diffScore) / numGames 
        winProb = sigmoid(scoreRate)

    return numWins, numLoses, numGames, totalWScore, totalLScore, diffScore, scoreRate, winProb



def predictTest(outfile, testData, trainData):
    with open(outfile, 'wb') as f:
        outcsv = csv.writer(f, delimiter=',')
        outcsv.writerow(['idName', 'numWins', 'numLoses', 'numGames',\
        'totalWScore', 'totalLScore', 'diffScore', 'scoreRate', 'winProb'])

        for item in testData['id']:
            season, targetTeam, compareTeam = item.split('_')

            if season == 'N':
                regularTrain = trainData.iloc[ 30702 : 59532, :]
            elif season == 'O':
                regularTrain = trainData.iloc[ 35321 : 64781, :]
            elif season == 'P':
                regularTrain = trainData.iloc[ 39893 : 70044, :]
            elif season == 'Q':
                regularTrain = trainData.iloc[ 44569 : 75291, :]
            elif season == 'R':
                regularTrain = trainData.iloc[ 49326 : 80544, :]

            #if season == 'N':
            #    regularTrain = trainData.iloc[ 445 : 829, :]
            #elif season == 'O':
            #    regularTrain = trainData.iloc[ 509 : 893, :]
            #elif season == 'P':
            #    regularTrain = trainData.iloc[ 573 : 957, :]
            #elif season == 'Q':
            #    regularTrain = trainData.iloc[ 637 : 1024, :]
            #elif season == 'R':
            #    regularTrain = trainData.iloc[ 701 : 1091, :]

            numWins, numLoses, numGames, totalWScore, totalLScore, diffScore,\
                  scoreRate, winProb \
                        = diffScores(regularTrain, str(season), int(targetTeam), int(compareTeam))
    
            record = [item, numWins, numLoses, numGames, totalWScore, totalLScore,\
                        diffScore, scoreRate, winProb]
            outcsv.writerow(record)


outRegular = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_scores.csv"
outTourney = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\tourney_scores.csv"
predictTest(outRegular, samples, regular)
#predictTest(outTourney, samples, tourney)

