import pandas
from numpy import *
from ggplot import *
import csv

def dataLoad(datafile):
    return pandas.read_csv(datafile)

def dataMerge(regular, tourney):

    left = pandas.DataFrame({'season': regular['season'], \
                             'r_daynum': regular['daynum'], \
                             'r_wteam': regular['wteam'], \
                             'r_wscore': regular['wscore'], \
                             'r_lteam': regular['lteam'], \
                             'r_lscore': regular['lscore'], \
                             'r_wloc': regular['wloc'], \
                             'r_numot': regular['numot']
                            })


    right = pandas.DataFrame({'season': tourney['season'], \
                             't_daynum': tourney['daynum'], \
                             't_wteam': tourney['wteam'], \
                             't_wscore': tourney['wscore'], \
                             't_lteam': tourney['lteam'], \
                             't_lscore': tourney['lscore'], \
                             't_numot': tourney['numot']
                            })

    fullData = pandas.merge(left, right, on='season')
    return fullData


regular = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\regular_season_results.csv"
tourney = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_results.csv"
samples = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\sample_submission.csv"
seeds = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_seeds.csv"
slots = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_slots.csv" 

regular = dataLoad(regular)
tourney = dataLoad(tourney)
samples = dataLoad(samples)
seeds = dataLoad(seeds)
slots = dataLoad(slots)


regular['diffScore'] = regular['wscore'] - regular['lscore'] 
tourney['diffScore'] = tourney['wscore'] - tourney['lscore']

