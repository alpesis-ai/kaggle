import pandas as pd
from numpy import *
from ggplot import *
import csv

def dataLoad(datafile):
    return pd.read_csv(datafile)


def cleanSeed(seeds):
    cleanSeeds = []
    for seed in seeds:
        seed = int(seed[1:3])
        cleanSeeds.append(seed)
    return cleanSeeds

def createTeamRank(seeds):
    teamRanks = {}
    teams = set(seeds['team'])
    for team in teams:
        teamSeeds = seeds[seeds['team'] == team]
        totalRanks = teamSeeds['seed'].sum()
        numGames = len(teamSeeds.index)
        teamRanks[team] = float(totalRanks) / numGames

    return teamRanks


def createDiffRanks(samples, teamRanks):
    diffRanks = {}
    for item in samples['id']:
        season, tTeam, cTeam = item.split('_')
        tTeam = int(tTeam)
        cTeam = int(cTeam)
        diffRank = teamRanks[tTeam] - teamRanks[cTeam]
        diffRanks[item] = diffRank
    return diffRanks

def probPredict(diffRanks):
    winProbs = {}
    for key in diffRanks.keys():
        winProbs[key] = 0.5 + 0.03 * diffRanks[key]
    return winProbs

def writeCSV(outPath, probDict):
    with open(outPath, 'w') as f:
        outcsv = csv.writer(f, delimiter=',')
        outcsv.writerow(['id', 'pred'])

        for key in probDict.keys():
            idName, pred = key, probDict[key]
            record = [idName, pred]
            outcsv.writerow(record)

def dataTrans(samples, winProbs):
    ids = []
    probs = []
    for key in winProbs.keys():
        ids.append(key)
        probs.append(winProbs[key])
    
    samples['id'] = ids
    samples['pred'] = probs
    return samples


seeds = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\tourney_seeds.csv"
samples = "G:\\vimFiles\\python\\kaggle\\MAR\\data\\sample_submission.csv"

seeds = dataLoad(seeds)
samples = dataLoad(samples)

seeds['seed'] = cleanSeed(seeds['seed'])
#print seeds['seed']
teamRanks = createTeamRank(seeds)
#print teamRanks
diffRanks = createDiffRanks(samples, teamRanks)
print diffRanks
winProbs = probPredict(diffRanks)

outPath = "G:\\vimFiles\\python\\kaggle\\MAR\\src\\outputs\\seed_probs.csv"
#writeCSV(outPath, winProbs)
#samples = dataTrans(samples, winProbs)
#print ggplot(aes(x='pred'), data=samples) + geom_histogram()
#samples.to_csv(outPath)
