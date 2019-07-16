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
# run a clustering alg in the new feature space from the pca
kmeans = KMeans()
kmeans.fit(npDataTrans)
nClusters = np.amax(kmeans.labels_) + 1
print("finding " + str(nClusters) + " clusters...")
################################################################################
# scatter plots showing clustering in first 2 PCA components
savePath="../figures/"
plt = plotting.scatter_2d(kmeans, npDataTrans)
playersToLabel =[
"curryst_2015","curryst_2016","curryst_2017","curryst_2018","curryst_2019",
"jamesle_2015","jamesle_2016","jamesle_2017","jamesle_2018","jamesle_2019",
"hardeja_2015","hardeja_2016","hardeja_2017","hardeja_2018","hardeja_2019",
"antetgi_2015","antetgi_2016","antetgi_2017","antetgi_2018","antetgi_2019"
"couside_2015","couside_2016","couside_2017","couside_2018","couside_2019"
]
plotting.add_labels_to_plot(plt, playersToLabel, idList, npDataTrans)
plt.savefig(savePath+"scatter2d.png", dpi=200); plt.clf();
################################################################################
# scatter plots showing clustering in first 3 PCA components
plt = plotting.scatter_3d(kmeans, npDataTrans)
plt.savefig(savePath+"scatter3d.png", dpi=200); plt.clf();
################################################################################
# visualize pca components
plt = plotting.vis_pca(pca, featureList)
plt.savefig(savePath+"pca_vis.png", dpi=100); plt.clf();
################################################################################
# plot team classifications over the years
#plt = plotting.classification_plot_teams(kmeans, npDataTrans, idList)
#plt.tight_layout()
#plt.savefig(savePath+"team_year.png", dpi=100); plt.clf();













#
