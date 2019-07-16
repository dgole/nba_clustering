#!/usr/bin/python
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import pandas
sys.path.append('../python/')
import tools
plt.rcParams['figure.figsize'] = [16, 11]
font = {'family' : 'DejaVu Sans',
		'weight' : 'normal',
		'size'   : 18}
mpl.rc('font', **font)
################################################################################
colorList = ['r','g','b','k','c','y','m','tab:gray']
################################################################################
def scatter_2d(kmeans, npDataTrans, colorList=colorList):
	'''
	Makes a scatter plot in a 2D space determined by the first
	two PCs.  Colors the points according to the cluster they
	belong to.
	'''
	nClusters = np.amax(kmeans.labels_)+1
	for n in range(nClusters):
		try:
			plt.scatter(kmeans.cluster_centers_[n,0],
						kmeans.cluster_centers_[n,1],
						marker="s", s=100, color=colorList[n])
		except: a=1
	for i in range(npDataTrans.shape[0]):
		label = kmeans.labels_[i]
		plt.scatter(npDataTrans[i,0],
					npDataTrans[i,1],
					marker=".", s=20, color=colorList[label])
	plt.axvline(x=0, color=(0,0,0,0.2))
	plt.axhline(y=0, color=(0,0,0,0.2))
	plt.xlabel("pc_0")
	plt.ylabel("pc_1")
	plt.tight_layout()
	return plt
################################################################################
def scatter_3d(kmeans, npDataTrans, colorList=colorList):
	'''
	Makes a scatter plot in a #D space determined by the first
	three PCs.  Colors the points according to the cluster they
    belong to.
	'''
	nClusters = np.amax(kmeans.labels_)+1
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for n in range(nClusters):
		try:
			ax.scatter(kmeans.cluster_centers_[n,0],
					   kmeans.cluster_centers_[n,1],
					   kmeans.cluster_centers_[n,2],
					   marker="s", s=100, color=colorList[n])
		except: a=1
	for i in range(npDataTrans.shape[0]):
		label = kmeans.labels_[i]
		ax.scatter(npDataTrans[i,0],
				   npDataTrans[i,1],
				   npDataTrans[i,2],
				   marker=".", s=10, color=colorList[label])
	ax.set_xlabel('pc_0')
	ax.set_ylabel('pc_1')
	ax.set_zlabel('pc_2')
	return plt
################################################################################
def vis_pca(pca, featureList):
	'''
	Visualizes the transform from the original feature space to the PCA
	determined feature space by making several bar graphs.
	'''
	fig, axs = plt.subplots(4, 1, figsize=(9, 12), sharex=True)
	for n in range(len(axs)):
		ax = axs[n]
		ax.bar(featureList, pca.components_[n])
		for tick in ax.get_xticklabels(): tick.set_rotation(60)
		ax.set_ylim(-0.8,0.8)
		ax.set_ylabel("pc_" + str(n))
	axs[0].set_title("Weights for the first 4 PCs")
	plt.tight_layout()
	return plt
################################################################################
def add_labels_to_plot(plt, labelList, idList, locs, fontsize=12):
	'''
	Adds player/team labels to an already existing scatter plot.
	'''
	for label in labelList:
		for n in range(len(idList)):
			if label==idList[n]:
				plt.annotate(label, locs[n,:2], fontsize=12)
################################################################################
def classification_plot_teams(kmeans, npDataTrans, idList):
	'''
	Visualizes the classification of each time for each season.
	'''
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
					marker="s", s=50, color=colorList[label])
	plt.yticks(range(len(tools.teamList)), tools.teamList)
	for n in range(1980,2020,5): plt.axvline(x=n, color=(0,0,0,0.1))
	plt.xlim(int(tools.seasonList[0][:4])+0.5, 2020-0.5)
	plt.ylim(-0.5, len(tools.teamList)-0.5)
	return plt

#
