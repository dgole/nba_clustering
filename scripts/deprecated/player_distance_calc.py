#!/usr/bin/python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import pandas as pd
sys.path.append('../python/')
import tools
import scrapers
import models
import plotting
################################################################################
# read in files and store as dfs in dict
season     = 2019
inPath     = "../data/players/"+str(season)+"/"
fileList   = os.listdir(inPath)
dfDict = {}
print("reading in player data from files...")
for fileName in fileList:
	df       = pd.read_csv(inPath + fileName)
	playerId = fileName[:-4]
	dfDict[playerId] = df
print(df)
################################################################################
# assemble features in numpy array
featureList = ["PTS","MP","2P%","2PA","3P%","3PA","FT%","FTA","ORB","DRB","AST",
			   "TOV","STL","BLK","PF"]
nFeatures      = len(featureList)
idList, npData = models.dict_to_np_players(dfDict, featureList)
npData         = models.scale_features(npData)
################################################################################
# fit pca and transform data
pca, npDataTrans = models.fit_pca(npData, 0.90)
################################################################################
# calculate distances between all teams and print min dist team
distMatrix = models.norm_dist_matrix(npDataTrans)
models.report_dist_matrix(distMatrix, idList)













#
