#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pandas
sys.path.append('./PandasBasketball/')
from PandasBasketball import pandasbasketball as pb
from basketball_reference_web_scraper import client
sys.path.append('./python/')
import tools
################################################################################
endYear = 2017
statsType = 'per_36'
################################################################################
# grab list of all players + stats for the season
allStats = client.players_season_totals(season_end_year=endYear)
playerNames = []
for stats in allStats: playerNames.append(stats['name'])
################################################################################
# look for names that don't get looked up right
n=0
nTot = len(playerNames)
allWeirdNames = []
for name in playerNames:
	print(str(n+1) + ' of ' + str(nTot))
	stats = tools.getPlayerStats(name, statsType=statsType)
	if stats is None:
		allWeirdNames.append(name)
		print(name)
	n+=1
print(allWeirdNames)
################################################################################
