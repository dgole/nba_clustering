#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import pandas
sys.path.append('../python/')
import tools
################################################################################
def fit_pca(npData, varRatioGoal):
	'''
	Uses sklean.pca to do a PCA analysis on the given numpy data.
	Returns the pca object as well as the transformed numpy data.
	Holds onto a number of PCs that explain varRatioGoal of the
	variance in the original data.
	'''
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
################################################################################
def scale_features(data):
	'''
	Scales each row of a 2d numpy array such that the span is one and
	the features are centered about zero.
	'''
	newData = np.zeros_like(data)
	for i in range(data.shape[1]):
		min  = np.amin(data[:,i])
		max  = np.amax(data[:,i])
		span = max-min
		mean = np.mean(data[:,i])
		newData[:,i] = (data[:,i]-mean)/span
	return newData
################################################################################
def norm_dist_matrix(npDataTrans):
	'''
	Returns a distance measurement matrix of shape nTeams x nTeams that
	contains the distance from each team to each other team in the
	given vector space.  Normalized such that the average distance is 1.
	Currently very computationally ineffecient.
	'''
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
	'''
	Prints out the nearest neighbor to each team/player given the distance matrix.
	'''
	for i in range(distMatrix.shape[0]):
		minDist = np.amin(distMatrix[i,:])
		minArg  = np.argmin(distMatrix[i,:])
		print("closest to " + idList[i] + ": " +
				  idList[minArg] + ", " + str(np.round(minDist,3)))
################################################################################
def sum_cluster_dist2(npDataTrans, kmeans, label):
	'''
	For a given data array, kmeans analysis, and label, return the sum of the
	squared distances from all points belonging to the given label to
	the center of the cluster.
	'''
	center        = kmeans.cluster_centers_[label]
	thisLabelArgs = np.nonzero(np.where(kmeans.labels_==label,1,0))
	thisData      = npDataTrans[thisLabelArgs]
	dist2         = np.sum(np.square(thisData-center))
	return dist2
def tot_sum_cluster_dists2(npDataTrans, kmeans):
	'''
	Calls sum_cluster_dist2 for each label and returns the sum of the
	squared distance sums for all clusters.
	'''
	dist2 = 0
	for label in kmeans.labels_:
		dist2 += sum_cluster_dist2(npDataTrans, kmeans, label)
	return dist2
def get_sorted_distances(loc, idList, npDataTrans, nPlayers):
	'''
	Returns a sorted list of nPlayers player IDs closest to loc, as well as
	the corresponding distances.
	'''
	dists         = np.sqrt(np.sum(np.square(npDataTrans-loc), axis=1))
	args          = np.argsort(dists)[:nPlayers]
	sortedDists   = dists[args]
	sortedIds     = []
	for arg in args: sortedIds.append(idList[arg])
	return (sortedIds, sortedDists)
################################################################################
def getSeasonIndex(endYear):
	startYear    = endYear-1
	endYearStr   = (str(endYear))[2:]
	startYearStr = str(startYear)
	indexStr     = startYearStr + '-' + endYearStr
	return indexStr
################################################################################
def dict_to_np_teams(dfDict, featureList):
	'''
	Takes a dictionary of pandas DFs containing team data and transforms it
	into a numpy array where each row is a team/season and each column
	contains a feature from featureList.
	'''
	nFeatures   = len(featureList)
	npData      = []
	idList      = []
	for team in tools.teamList:
		df = dfDict[team]
		for season in tools.seasonList:
			seasonDf = df[df["Season"]==season]
			if not seasonDf.empty and not seasonDf.isnull().values.any():
				thisRow = np.zeros(nFeatures)
				n = 0
				for feature in featureList:
					if feature == "Ht.":
						value = tools.convert_height_str(seasonDf[feature].values[0])
					else:
						value = seasonDf[feature].values[0]
					thisRow[n] = value
					n+=1
				npData.append(thisRow)
				endYear = season[:2] + season[5:]
				endYear = int(endYear)
				if endYear == 1900: endYear = 2000
				idList.append(team + "_" + str(endYear))
	npData = np.asarray(npData)
	return idList, npData

def dict_to_np_players(dfDict, featureList):
	'''
	Takes a dictionary of pandas DFs containing player data and transforms it
	into a numpy array where each row is a team/season and each column
	contains a feature from featureList.
	'''
	nFeatures   = len(featureList)
	npData      = []
	idList      = []
	for playerId in dfDict.keys():
		df = dfDict[playerId]
		#print(df)
		for season in df['Season'].values:
			seasonDf = df[df["Season"]==season]
			if not seasonDf.empty and not seasonDf.isnull().values.any():
				thisRow = np.zeros(nFeatures)
				n = 0
				for feature in featureList:
					if feature == "Ht.":
						value = tools.convert_height_str(seasonDf[feature].values[0])
					else:
						try:
							value = seasonDf[feature].values[0]
						except:
							value = 0.0
					thisRow[n] = value
					n+=1
				npData.append(thisRow)
				endYear = season[:2] + season[5:]
				endYear = int(endYear)
				if endYear == 1900: endYear = 2000
				idList.append(playerId[:-2] + "_" + str(endYear))
	npData = np.asarray(npData)
	return idList, npData






#
