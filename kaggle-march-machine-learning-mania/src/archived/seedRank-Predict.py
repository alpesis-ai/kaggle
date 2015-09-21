

import pandas
from numpy import *
from ggplot import *
import csv
import math

def dataLoad(datafile):
    return pandas.read_csv(datafile)


def cleanSeed(seeds):
    cleanSeeds = []
    for seed in seeds:
        seed = int(seed[1:3])
        cleanSeeds.append(seed)
    return cleanSeeds

def sigmoid(z):
    return 1.0/(1+exp(-z))

def rating(rank):
    return 100 - 4 * math.log(rank+1) - rank/22.0

def logisticProb(diffRating):
    diff = - diffRating / 15.0 
    powerDiff = math.pow(10, diff)
    return 1.0 / (1 + powerDiff)


def predict(samples, seeds, outPath):
    with open(outPath, 'wb') as f:
        outfile = csv.writer(f, delimiter=',')
        outfile.writerow(['id', 'diffRating', 'pred'])
        

        for item in samples['id']:
            season, tteam, cteam = item.split('_')
            tteam = int(tteam)
            cteam = int(cteam)

            if season == "N":
                ratings = seeds.iloc[ 517 : 842, :]
            elif season == "O":
                ratings = seeds.iloc[ 582 : 907, :]
            elif season == "P":
                ratings = seeds.iloc[ 647 : 972, :]
            elif season == "Q":
                ratings = seeds.iloc[ 712 : 1040, :]
            elif season == "R":
               ratings = seeds.iloc[ 777 : 1108, :]

            tRating = ratings[ratings['team'] == tteam]
            cRating = ratings[ratings['team'] == cteam]

            tteamRating = tRating['rating'].sum()
            cteamRating = cRating['rating'].sum()

            numtteam = len(tRating.index)
            numcteam = len(cRating.index)

            if (numtteam == 0) or (numcteam == 0):
                diffRating = 0
            else:
                avgtteam = float(tteamRating) / numtteam
                avgcteam = float(cteamRating) / numcteam
                diffRating = avgtteam - avgcteam

            winProb = logisticProb(diffRating)

            record = [item, diffRating, winProb]
            outfile.writerow(record)

    f.close()

seeds = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_seeds.csv"
samples = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\sample_submission.csv"

seeds = dataLoad(seeds)
samples = dataLoad(samples)

seeds['seed'] = cleanSeed(seeds['seed'])
#print seeds.head(10)

seeds['rating'] = 100 - 4 * log(seeds['seed']+1) - seeds['seed']/22.0
outPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\seedPredict.csv"
predict(samples, seeds, outPath)
