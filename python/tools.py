#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import pandas
#sys.path.append('./PandasBasketball/')
#from PandasBasketball import pandasbasketball as pb
#from basketball_reference_web_scraper import client
################################################################################
seasonList = [str(n) + "-" + str(n+1)[2:] for n in range(1979, 2020)]
teamList = ["NJN","CHA","NOH","ATL","BOS","CHI","CLE","DET",
			"IND","MIA","MIL","NYK","ORL","PHI","TOR","WAS","DAL","DEN","GSW",
			"HOU","LAC","LAL","MEM","MIN","OKC","PHO","POR","SAC","SAS","UTA"]
teamList.sort()
champIds = [
			"LAL_1980","BOS_1981","LAL_1982","PHI_1983","BOS_1984",
			"LAL_1985","BOS_1986","LAL_1987","LAL_1988","DET_1989",
			"DET_1990","CHI_1991","CHI_1992","CHI_1993","HOU_1994",
			"HOU_1995","CHI_1996","CHI_1997","CHI_1998","SAS_1999",
			"LAL_2000","LAL_2001","LAL_2002","SAS_2003","DET_2004",
			"SAS_2005","MIA_2006","SAS_2007","BOS_2008","LAL_2009",
			"LAL_2010","DAL_2011","MIA_2012","MIA_2013","SAS_2014",
			"GSW_2015","CLE_2016","GSW_2017","GSW_2018","GSW_2019"
]
################################################################################
def fit_pca(npData, varRatioGoal):
	# fit PCA to data and choose how many components are needed
	pca = PCA()
	pca.fit(npData)
	varRatio = pca.explained_variance_ratio_
	varTot = 0.0
	for n in range(npData.shape[1]):
		varTot += varRatio[n]
		if varTot > varRatioGoal:
			nComps = n+1
			break
	print("Using " + str(nComps) + " components explaining " + str(varTot*100) +
		  "% of variance in original data set")
	############################################################################
	# fit PCA with only nComps components
	pca = PCA(n_components=nComps)
	pca.fit(npData)
	############################################################################
	# transform original feature vector into new space with only nComps features
	npDataTrans = pca.transform(npData)
	return pca, npDataTrans

def scale_features(data):
	newData = np.zeros_like(data)
	for i in range(data.shape[1]):
		min  = np.amin(data[:,i])
		max  = np.amax(data[:,i])
		span = max-min
		mean = np.mean(data[:,i])
		newData[:,i] = (data[:,i]-mean)/span
	return newData

def norm_dist_matrix(npDataTrans):
	nTeams     = npDataTrans.shape[0]
	distMatrix = np.zeros([nTeams, nTeams])
	for i in range(nTeams):
		for j in range(nTeams):
			feats1 = npDataTrans[i]
			feats2 = npDataTrans[j]
			dist   = np.sqrt(np.sum(np.square(feats1-feats2)))
			distMatrix[i,j] = dist
	for i in range(nTeams):
		distMatrix[i,i] = np.mean(distMatrix[i,:])
	meanDist    = np.mean(distMatrix)
	distMatrix /= meanDist
	return distMatrix

def report_dist_matrix(distMatrix, idList):
	for i in range(distMatrix.shape[0]):
		minDist = np.amin(distMatrix[i,:])
		minArg  = np.argmin(distMatrix[i,:])
		print("team closest to " + idList[i] + ": " +
				  idList[minArg] + ", " + str(np.round(minDist,3)))

def convert_height_str(s):
	feet   = float(s[0])
	inches = float(s[2:])
	tot    = feet + inches/12.0
	return tot

def scatter_2d(kmeans, npDataTrans, colors):
	nClusters = np.amax(kmeans.labels_)+1
	for n in range(nClusters):
		plt.scatter(kmeans.cluster_centers_[n,0],
					kmeans.cluster_centers_[n,1],
					marker="s", s=50, color=colors[n])
	for i in range(npDataTrans.shape[0]):
		label = kmeans.labels_[i]
		plt.scatter(npDataTrans[i,0],
					npDataTrans[i,1],
					marker=".", s=10, color=colors[label])
	plt.axvline(x=0, color=(0,0,0,0.2))
	plt.axhline(y=0, color=(0,0,0,0.2))
	plt.xlabel("pc_0")
	plt.ylabel("pc_1")
	plt.tight_layout()
	return plt
	#plt.savefig(savePath+"scatter2d.png", dpi=200); plt.clf();

def scatter_3d(kmeans, npDataTrans, colors):
	nClusters = np.amax(kmeans.labels_)+1
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for n in range(nClusters):
		ax.scatter(kmeans.cluster_centers_[n,0],
					kmeans.cluster_centers_[n,1],
					kmeans.cluster_centers_[n,2],
					marker="s", s=100, color=colors[n])
	for i in range(npDataTrans.shape[0]):
		label = kmeans.labels_[i]
		ax.scatter(npDataTrans[i,0],
					npDataTrans[i,1],
					npDataTrans[i,2],
					marker=".", s=10, color=colors[label])
	ax.set_xlabel('pc_0')
	ax.set_ylabel('pc_1')
	ax.set_zlabel('pc_2')
	return plt
	#plt.savefig(savePath+"scatter3d.png", dpi=200); plt.clf();

def vis_pca(pca, featureList):
	fig, axs = plt.subplots(4, 1, figsize=(9, 12), sharex=True)
	for n in range(len(axs)):
		ax = axs[n]
		ax.bar(featureList, pca.components_[n])
		for tick in ax.get_xticklabels(): tick.set_rotation(60)
		ax.set_ylim(-0.8,0.8)
	plt.tight_layout()
	return plt
	#plt.savefig(savePath+"pca_vis.png", dpi=100); plt.clf();

def add_labels_to_plot(plt, labelList, idList, locs):
	for label in labelList:
		for n in range(len(idList)):
			if label==idList[n]:
				plt.annotate(label, locs[n,:2], fontsize=5)






















posList = ['PG', 'SG', 'SF', 'PF', 'C']

class Game:
	def __init__(self, s, endYear):
		self.s = s
		self.endYear = endYear
		self.homeTeam  = s['home_team']
		self.awayTeam  = s['away_team']
		self.homeScore = s['home_team_score']
		self.awayScore = s['away_team_score']
		if self.homeScore > self.awayScore:	self.winner = 1
		else:								self.winner = 0
		self.year    = s['start_time'].year
		self.month   = s['start_time'].month
		self.day     = s['start_time'].day
		self.badGame = 0
		self.seasonIndex = getSeasonIndex(self.endYear)
	def addRosters(self):
		self.homeTeamPlayerNames = []
		self.awayTeamPlayerNames = []
		players = client.player_box_scores(day=self.day, month=self.month, year=self.year)
		for player in players:
			if   player['team'] == self.homeTeam:
				self.homeTeamPlayerNames.append(player['name'])
			elif player['team'] == self.awayTeam:
				self.awayTeamPlayerNames.append(player['name'])
		if len(self.homeTeamPlayerNames)<2 or len(self.awayTeamPlayerNames)<2:
			players = client.player_box_scores(day=max(self.day-1,0), month=self.month, year=self.year)
			for player in players:
				if   player['team'] == self.homeTeam:
					self.homeTeamPlayerNames.append(player['name'])
				elif player['team'] == self.awayTeam:
					self.awayTeamPlayerNames.append(player['name'])
		if len(self.homeTeamPlayerNames)<2 or len(self.awayTeamPlayerNames)<2:
			players = client.player_box_scores(day=self.day+1, month=self.month, year=self.year)
			for player in players:
				if   player['team'] == self.homeTeam:
					self.homeTeamPlayerNames.append(player['name'])
				elif player['team'] == self.awayTeam:
					self.awayTeamPlayerNames.append(player['name'])
		if len(self.homeTeamPlayerNames)<2 or len(self.awayTeamPlayerNames)<2:
			players = client.player_box_scores(day=max(self.day-2,0), month=self.month, year=self.year)
			for player in players:
				if   player['team'] == self.homeTeam:
					self.homeTeamPlayerNames.append(player['name'])
				elif player['team'] == self.awayTeam:
					self.awayTeamPlayerNames.append(player['name'])
		if len(self.homeTeamPlayerNames)<2 or len(self.awayTeamPlayerNames)<2:
			self.badGame = 1
	def addPlayerAdvStats(self):
		self.homeTeamAdvStats = []
		self.awayTeamAdvStats = []
		for name in self.homeTeamPlayerNames:
			stats = getPlayerStats(name, statsType='advanced')
			if stats is not None: self.homeTeamAdvStats.append(stats)
			else:                 self.badGame = 1
		for name in self.awayTeamPlayerNames:
			stats = getPlayerStats(name, statsType='advanced')
			if stats is not None: self.awayTeamAdvStats.append(stats)
			else:                 self.badGame = 1
	def setLineups(self):
		self.lineupStatsHome = {}
		starterStats = 0
		for pos in posList:
			mins = 0
			for stats in self.homeTeamAdvStats:
				temp = stats.loc[stats['Season'] == self.seasonIndex]
				if temp.shape[0]>1:
					temp  = temp.loc[temp['Tm'] == 'TOT']
					thisPos  = temp['Pos'].as_matrix()[0]
					thisMins = temp['MP'].as_matrix()[0]
				elif temp.shape[0]==1:
					thisPos  = temp['Pos'].as_matrix()[0]
					thisMins = temp['MP'].as_matrix()[0]
				else:
					thisPos = 'x'
					thisMins = 0
				if thisPos == pos and thisMins > mins:
					benchStats   = starterStats
					starterStats = temp
					mins         = thisMins
			self.lineupStatsHome[pos+'0'] = starterStats
			self.lineupStatsHome[pos+'1'] = benchStats
		self.lineupStatsAway = {}
		starterStats = 0
		for pos in posList:
			mins = 0
			for stats in self.awayTeamAdvStats:
				temp = stats.loc[stats['Season'] == self.seasonIndex]
				if temp.shape[0]>1:
					temp  = temp.loc[temp['Tm'] == 'TOT']
					thisPos  = temp['Pos'].as_matrix()[0]
					thisMins = temp['MP'].as_matrix()[0]
				elif temp.shape[0]==1:
					thisPos  = temp['Pos'].as_matrix()[0]
					thisMins = temp['MP'].as_matrix()[0]
				else:
					thisPos = 'x'
					thisMins = 0
				if thisPos == pos and thisMins > mins:
					benchStats   = starterStats
					starterStats = temp
					mins         = thisMins
			self.lineupStatsAway[pos+'0'] = starterStats
			self.lineupStatsAway[pos+'1'] = benchStats



def getPlayerLookupString(playerName):
	if playerName in weirdNamesLookup:
		return weirdNamesLookup[playerName]
	else:
		# find space to seperate first and last name
		spaceIndex = 0
		for char in playerName:
			if char == ' ':	break
			spaceIndex+=1
		firstName = playerName[:spaceIndex]
		lastName  = playerName[spaceIndex+1:]
		# remove dots and apostrophies from names
		firstNameNew = []
		lastNameNew  = []
		for char in firstName:
			if char!='.' and char!="'":
				firstNameNew.append(char)
		firstNameNew = ''.join(firstNameNew)
		for char in lastName:
			if char!='.' and char!="'":
				lastNameNew.append(char)
		lastNameNew = ''.join(lastNameNew)
		# lookup string is <last name first 5 chars><first name first 2 chars><01>
		if len(lastNameNew)<6: lastLookupStr = lastNameNew
		else:				   lastLookupStr = lastNameNew[:5]
		firstLookupStr = firstNameNew[:2]
		lookupStr = lastLookupStr.lower() + firstLookupStr.lower() + '01'
		return lookupStr

def getPlayerStats(playerName, statsType='per_game'):
	lookup = getPlayerLookupString(playerName)
	try:
		#stats = pb.get_player(lookup, statsType, numeric=True, s_index=True)
		stats = pb.get_player(lookup, statsType, numeric=True)
	except:
		print('failed to get stats for lookup string: ' + lookup)
		print('full name was ' + playerName)
		stats = None
	return stats

################################################################################

weirdNamesLookup = {
	'J.J. Barea': 'bareajo01',
	'Nicolas Batum': 'batumni01',
	'Clint Capela': 'capelca01',
	'Michael Kidd-Gilchrist': 'kiddgmi01',
	'Sheldon Mac': 'mcclesh01',
	'Luc Mbah a Moute': 'mbahalu01',
	'James Michael McAdoo': 'mcadoja01',
	'Edy Tavares': 'tavarwa01',
	'Taurean Waller-Prince': 'princta02',
	'Metta World Peace': 'artesro01',
}

def getSeasonIndex(endYear):
	startYear    = endYear-1
	endYearStr   = (str(endYear))[2:]
	startYearStr = str(startYear)
	indexStr     = startYearStr + '-' + endYearStr
	return indexStr






#
