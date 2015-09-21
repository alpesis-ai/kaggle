#-----------------------------------------------------#
# Project: Mar
# Author: Kelly Chan
# Date: Apr 1 2014
#-----------------------------------------------------#

dataPath = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\stage2\\"
cleanDataPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\data\\"
outPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\"
tempPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\tables\\temp.csv"


import pandas as pd
import numpy as np

def loadData(datafile):
    return pd.read_csv(datafile)

def printData(data):
    print data.head(5)

def mergeTourney(tourney_results, tourney_seeds):
    tourney = pd.merge(tourney_results, tourney_seeds, left_on=['season', 'wteam'], \
                                                       right_on=['season', 'team'], \
                                                       how='left')
    tourney = pd.merge(tourney, tourney_seeds, left_on=['season', 'lteam'], \
                                                       right_on=['season', 'team'], \
                                                       how='left')
    tourney['wseed'] = tourney['seed_x'].str[1:3].astype(int)
    tourney['lseed'] = tourney['seed_y'].str[1:3].astype(int)
    tourney = tourney.drop(['seed_x', 'team_x', 'seed_y', 'team_y'], axis=1)
    
    return tourney

def calDiff(tourney):

    tourney['seedDiff'] = (tourney['wseed'] - tourney['lseed']).abs()
    tourney['scoreDiff'] = tourney['wscore'] - tourney['lscore']

    tourney['rating'] = tourney['scoreDiff'] + (tourney['scoreDiff'] * tourney['seedDiff'])

    return tourney


def calTeamScores(teams, tourney):

    winData = tourney.loc[:, ['wteam', 'rating']]
    lossData = tourney.loc[:, ['lteam', 'rating']]

    winData = winData.groupby('wteam').sum()
    lossData = lossData.groupby('lteam').sum()

    winData = winData.reset_index()
    lossData = lossData.reset_index()

    teamRating = pd.merge(teams, winData, left_on='id', right_on='wteam', how='left')
    teamRating = pd.merge(teamRating, lossData, left_on='id', right_on='lteam', how='left')
    teamRating = teamRating.drop(['wteam', 'lteam'], axis=1)
    teamRating = teamRating.rename(columns={'rating_x': 'wrating', 'rating_y': 'lrating'})
    teamRating = teamRating.fillna(0)
    
    teamRating['rating'] = teamRating['wrating'] - teamRating['lrating']
    teamRating = teamRating.drop(['wrating', 'lrating'], axis=1)


    return teamRating



def mergeRating(sample_submission, teamRating):

    sample_submission['team1'] = sample_submission['id'].str[2:5].astype(int)
    sample_submission['team2'] = sample_submission['id'].str[6:].astype(int)

    sample_submission = pd.merge(sample_submission, teamRating, left_on=['team1'], \
                                                                right_on=['id'], \
                                                                how='left')

    sample_submission = pd.merge(sample_submission, teamRating, left_on=['team2'], \
                                                                right_on=['id'], \
                                                                how='left')

    sample_submission['ratingDiff'] = sample_submission['rating_x'] - sample_submission['rating_y']
    sample_submission = sample_submission.drop(['rating_x', 'team1', 'id', 'name_x', \
                                                'rating_y', 'team2', 'id_y', 'name_y'], \
                                                axis=1)

    return sample_submission




def predictProb(sample_submission):

    sample_submission['pred'] = 1 - 1. / ( 1. + 10**(sample_submission['ratingDiff']/400.))
    return sample_submission


def main():

    teams = loadData(dataPath + "teams.csv")
    tourney_seeds = loadData(dataPath + "tourney_seeds.csv")
    tourney_results = loadData(dataPath + "tourney_results.csv")
    sample_submission = loadData(dataPath + "sample_submission.csv")

    tourney = mergeTourney(tourney_results, tourney_seeds)
    tourney = calDiff(tourney)

    teamRating = calTeamScores(teams, tourney)
    sample_submission = mergeRating(sample_submission, teamRating)

    submission = predictProb(sample_submission)
    submission.to_csv(tempPath)

    
if __name__ == "__main__":
    main()
