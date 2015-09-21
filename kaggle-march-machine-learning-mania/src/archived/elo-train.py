#----------------------------------------------------#
# Project: March Machine Learning Mania 
# Author: Kelly Chan
# Date: Mar 15 2014
#----------------------------------------------------#

'''
diffScore = sum(wscore-lscore) / numGames
ratingScore = 0.5 * diffScore_regular + 0.5 * diffScore_tourney  
latest_rating = lastRating + (thisRating - lastRating)
'''


import pandas
from numpy import *
from ggplot import *
import csv



def dataLoad(datafile):
    return pandas.read_csv(datafile)

def ratingScore(teams, data):
    teamRating = {}
    for team in teams['id']:
        wteamData = data[data['wteam'] == team]
        lteamData = data[data['lteam'] == team]

        wScore = wteamData['diffScore'].sum()
        lScore = lteamData['diffScore'].sum()
        totalScore = wScore - lScore

        wGames = len(wteamData.index)
        lGames = len(lteamData.index)
        numGames = wGames + lGames

        if numGames == 0:
            teamRating[team] = 0
        else:
            teamRating[team] = float(totalScore) / numGames

    return teamRating


def yearRating(regularRating, tourneyRating):
    teamRating = {}

    for key in regularRating.keys():
        teamRating[key] = regularRating[key] 

    for key in tourneyRating.keys():
        teamRating[key] += tourneyRating[key] * 2 

    return teamRating


def seasonRating(teams, regular, tourney, outPath):
    with open(outPath, 'wb') as f:
        outfile = csv.writer(f, delimiter=',')
        outfile.writerow(['season', 'team', 'regular', 'tourney', 'rating'])

        for season in set(tourney['season']):
            seasonRegular = ratingScore(teams, regular[regular['season'] == season])
            seasonTourney = ratingScore(teams, tourney[tourney['season'] == season])
            seasonRating = yearRating(seasonRegular, seasonTourney)

            for key in seasonRating.keys():
                record = [season, key, seasonRegular[key], seasonTourney[key], seasonRating[key]]
                outfile.writerow(record)

    f.close()


def createRatingSummary(seasonRatings, ratingPath):
    seasonRatings = seasonRatings.loc[:, ['season', 'team', 'rating']]
    ratingSummary = pandas.pivot_table(seasonRatings, values='rating', \
                                        rows=['team'], \
                                        cols=['season'])
    ratingSummary.index.name = 'team'
    ratingSummary = ratingSummary.reset_index()
    ratingSummary.to_csv(ratingPath)




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

regular['diffScore'] = regular['wscore'] - regular['lscore']
tourney['diffScore'] = tourney['wscore'] - tourney['lscore']

outPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\ratings\\seasonRatings.csv"
seasonRating(teams, regular, tourney, outPath)

ratingPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\ratings\\ratingSummary.csv"
seasonRatings = dataLoad(outPath)
createRatingSummary(seasonRatings, ratingPath)




seasonA = ratingSummary['A'] 
seasonB = seasonA + (ratingSummary['B'] - ratingSummary['A']) 
seasonC = seasonB + (ratingSummary['C'] - ratingSummary['B']) 
seasonD = seasonC + (ratingSummary['D'] - ratingSummary['C']) 
seasonE = seasonD + (ratingSummary['E'] - ratingSummary['D']) 
seasonF = seasonE + (ratingSummary['F'] - ratingSummary['E']) 
seasonG = seasonF + (ratingSummary['G'] - ratingSummary['F']) 
seasonH = seasonG + (ratingSummary['H'] - ratingSummary['G']) 
seasonI = seasonH + (ratingSummary['I'] - ratingSummary['H']) 
seasonJ = seasonI + (ratingSummary['J'] - ratingSummary['I']) 
seasonK = seasonJ + (ratingSummary['K'] - ratingSummary['J']) 
seasonL = seasonK + (ratingSummary['L'] - ratingSummary['K']) 
seasonM = seasonL + (ratingSummary['M'] - ratingSummary['L']) 
seasonN = seasonM + (ratingSummary['N'] - ratingSummary['M']) 
seasonO = seasonN + (ratingSummary['O'] - ratingSummary['N']) 
seasonP = seasonO + (ratingSummary['P'] - ratingSummary['O']) 
seasonQ = seasonP + (ratingSummary['Q'] - ratingSummary['P']) 
seasonR = seasonQ + (ratingSummary['R'] - ratingSummary['Q']) 
#seasonS = seasonR + (ratingSummary['S'] - ratingSummary['R']) * 2



finalRatings = pandas.DataFrame({ 'team' : ratingSummary['team'],
                                  'seasonA' : seasonA,
                                  'seasonB' : seasonB,
                                  'seasonC' : seasonC,
                                  'seasonD' : seasonD,
                                  'seasonE' : seasonE,
                                  'seasonF' : seasonF,
                                  'seasonG' : seasonG,
                                  'seasonH' : seasonH,
                                  'seasonI' : seasonI,
                                  'seasonJ' : seasonJ,
                                  'seasonK' : seasonK,
                                  'seasonL' : seasonL,
                                  'seasonM' : seasonM,
                                  'seasonN' : seasonN,
                                  'seasonO' : seasonO,
                                  'seasonP' : seasonP,
                                  'seasonQ' : seasonQ,
                                  'seasonR' : seasonR
                                })
print finalRatings.head(10)

finalPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\ratings\\finalRatings.csv"
finalRatings.to_csv(finalPath)
