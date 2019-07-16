#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import pandas
################################################################################
seasonList = [str(n) + "-" + str(n+1)[2:] for n in range(1979, 2020)]
#seasonList = [str(n) + "-" + str(n+1)[2:] for n in range(2010, 2020)]
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
thisSeasonIds = [teamList[n]+"_"+"2019" for n in range(len(teamList))]
################################################################################
def convert_height_str(s):
	'''
	Converts height from a string (ie. 6'8'') to a float in inches.
	'''
	feet   = float(s[0])
	inches = float(s[2:])
	tot    = feet + inches/12.0
	return tot
################################################################################
def getSeasonIndex(endYear):
	'''
	Takes the end year of a season and returns startYear-endYear
	'''
	startYear    = endYear-1
	endYearStr   = (str(endYear))[2:]
	startYearStr = str(startYear)
	indexStr     = startYearStr + '-' + endYearStr
	return indexStr
################################################################################
def get_player_lookup_string(playerName):
	'''
	Takes a player name with no special formatting and returns their
	player lookup string for bball ref.  ie. "Lebron James" --> "jamesle01".
	'''
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




#
