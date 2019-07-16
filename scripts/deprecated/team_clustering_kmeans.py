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
# scrape data and store as dfs in dict
print("scraping all seasons for all teams...")
dfDict = scrapers.scrape_all_teams(tools.teamList)
################################################################################
# assemble features in numpy array
featureList = ["W","PTS","2P%","2PA","3P%","3PA","FT%","FTA","ORB","DRB","AST",
			   "TOV","STL","BLK","PF","Age","Ht.","Wt."]
nFeatures      = len(featureList)
idList, npData = models.dict_to_np_teams(dfDict, featureList)
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
#plotting.add_labels_to_plot(plt, tools.champIds, idList, npDataTrans)
plotting.add_labels_to_plot(plt, tools.thisSeasonIds, idList, npDataTrans)
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
plt = plotting.classification_plot_teams(kmeans, npDataTrans, idList)
plt.tight_layout()
plt.savefig(savePath+"team_year.png", dpi=100); plt.clf();













#
