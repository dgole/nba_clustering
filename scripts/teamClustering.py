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
import scraper
################################################################################
# scrape data and store as dfs in dict
dfDict = {}
for team in tools.teamList:
	print(team)
	df           = scraper.get_team_stats_basic(team)
	dfDict[team] = df
print(dfDict["CLE"])
################################################################################
# assemble features in numpy array
featureList = ["W","PTS",
			   "2P%","2PA","3P%","3PA","FT%","FTA",
			   "ORB","DRB","AST","TOV",
			   "STL","BLK","PF",
			   "Age","Ht.","Wt."
			   ]
nFeatures      = len(featureList)
idList, npData = scraper.dict_to_np(dfDict, featureList)
npData         = tools.scale_features(npData)
################################################################################
# fit pca and transform data
pca, npDataTrans = tools.fit_pca(npData, 0.95)
################################################################################
# calculate distances between all teams and print min dist team
#distMatrix = tools.norm_dist_matrix(npDataTrans)
#tools.report_dist_matrix(distMatrix, idList)
################################################################################
# run a clustering alg in the new feature space from the pca
kmeans = KMeans()
kmeans.fit(npDataTrans)
nClusters = np.amax(kmeans.labels_) + 1
print("finding " + str(nClusters) + " clusters...")
################################################################################
# scatter plots showing clustering in first 2 PCA components
savePath="../figures/"
colors = ['r','g','b','k','c','y','m','tab:gray']
plt = tools.scatter_2d(kmeans, npDataTrans, colors)
tools.add_labels_to_plot(plt, tools.champIds, idList, npDataTrans)
plt.savefig(savePath+"scatter2d.png", dpi=200); plt.clf();
################################################################################
# scatter plots showing clustering in first 3 PCA components
plt = tools.scatter_3d(kmeans, npDataTrans, colors)
plt.savefig(savePath+"scatter3d.png", dpi=200); plt.clf();
################################################################################
# visualize pca components
plt = tools.vis_pca(pca, featureList)
plt.savefig(savePath+"pca_vis.png", dpi=100); plt.clf();
################################################################################
# plot team classifications over the years
for i in range(npDataTrans.shape[0]):
	team = idList[i][:3]
	for n in range(len(tools.teamList)):
		if team == tools.teamList[n]:
			teamNum = n
			break
	year = int(idList[i][4:])
	label = kmeans.labels_[i]
	plt.scatter(year,
				teamNum,
				marker="s", s=50, color=colors[label])
plt.yticks(range(len(tools.teamList)), tools.teamList)
for n in range(1980,2020,5): plt.axvline(x=n, color=(0,0,0,0.2))
plt.xlim(1979, 2020)
plt.ylim(-1, len(tools.teamList))
plt.tight_layout()
plt.savefig(savePath+"team_year.png", dpi=100); plt.clf();













#
