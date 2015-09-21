#----------------------------------------------------#
# Project: March Machine Learning Mania 
# Author: Kelly Chan
# Date: Mar 15 2014
#----------------------------------------------------#

'''
diffScore = sum(wscore-lscore) / numGames
ratingScore = 0.3 * diffScore_regular + 0.7 * diffScore_tourney  
latest_rating = lastRating + (thisRating - lastRating) * 2

WinPct(RatingDiff) = 1/(1+POWER(10,-RatingDiff/15))
'''


import pandas
from numpy import *
from ggplot import *
import csv



def dataLoad(datafile):
    return pandas.read_csv(datafile)

def logisticProb(diffRating):
    diff = - diffRating / 20.0 
    powerDiff = math.pow(10, diff)
    return 1.0 / (1 + powerDiff)

def sigmoid(z):
    return 1.0/(1+exp(-z))

def predict(samples, finalRatings, outPath):
    with open(outPath, 'wb') as f:
        outfile = csv.writer(f, delimiter=',')
        outfile.writerow(['id', 'diffRating', 'pred'])
        

        for item in samples['id']:
            season, tteam, cteam = item.split('_')
            tteam = int(tteam)
            cteam = int(cteam)

            if season == "N":
                ratings = finalRatings.loc[:, ['team', 'seasonM']]
            elif season == "O":
                ratings = finalRatings.loc[:, ['team', 'seasonN']]
            elif season == "P":
                ratings = finalRatings.loc[:, ['team', 'seasonO']]
            elif season == "Q":
                ratings = finalRatings.loc[:, ['team', 'seasonP']]
            elif season == "R":
               ratings = finalRatings.loc[:, ['team', 'seasonQ']]

            tRating = ratings[ratings['team'] == tteam]
            cRating = ratings[ratings['team'] == cteam]

            tteamRating = tRating.iloc[0,1]
            cteamRating = cRating.iloc[0,1]

            diffRating = tteamRating - cteamRating
            winProb = sigmoid(diffRating / 20.0)

            record = [item, diffRating, winProb]
            outfile.writerow(record)

    f.close()



samples = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\sample_submission.csv"
finalRatings = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\ratings\\finalRatings.csv"
finalRatings = dataLoad(finalRatings)
samples = dataLoad(samples)
#print finalRatings.head(5)

outPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\ratings\\winProbs.csv"
predict(samples, finalRatings, outPath)
