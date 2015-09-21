
import pandas as pd
from numpy import *
from ggplot import *


def dataLoad(datafile):
    return pd.read_csv(datafile)

def sigmoid(z):
    return 1.0/(1+exp(-z))

def finalScore(regularScore, tourneyScore):
    return 0.3 * regularScore + 0.7 * tourneyScore



regular = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\regular_scores.csv"
tourney = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\tourney_scores.csv"
outfile = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\final_scores.csv"

regular = dataLoad(regular)
tourney = dataLoad(tourney)



regular['finalScore'] = finalScore(regular['scoreRate'], tourney['scoreRate'])
regular['finalProb'] = sigmoid(regular['finalScore'] / 15.0)

regular.to_csv(outfile)

#print ggplot(aes(x='winProb', y='finalProb'), data=regular) + geom_point()
print ggplot(aes(x='finalProb'), data=regular) + geom_histogram()
