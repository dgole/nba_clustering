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
idList, npData = scrapers.dict_to_np(dfDict, featureList)
npData         = models.scale_features(npData)
################################################################################
# fit pca and transform data
pca, npDataTrans = models.fit_pca(npData, 0.90)
################################################################################
# calculate distances between all teams and print min dist team
distMatrix = tools.norm_dist_matrix(npDataTrans)
tools.report_dist_matrix(distMatrix, idList)













#
