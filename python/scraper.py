import numpy as np
import os
import sys
import pandas as pd
import tools
import requests
from bs4 import BeautifulSoup
################################################################################
BASE_URL = "https://www.basketball-reference.com"

def get_team_stats_basic(team):
    url = BASE_URL + "/teams/" + team + "/stats_per_game_totals" + ".html"
    r = requests.get(url)
    if r.status_code == 404:
        print("page not found")
    else:
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll("table")
        if len(tables) == 1: table = tables[0]
        else: print("More than one table found, don't know what to do")
        columns = []
        heading = table.find("thead")
        heading_row = heading.find("tr")
        for x in heading_row.find_all("th"):
            columns.append(x.string)
        body = table.find("tbody")
        rows = body.find_all("tr")
        data = []
        for row in rows:
            temp = []
            th = row.find("th")
            td = row.find_all("td")
            if th:
                temp.append(th.text)
            else:
                continue
            for v in td:
                temp.append(v.text)
            data.append(temp)
        for l in data:
            if len(l) < 2:
                data.remove(l)
        df = pd.DataFrame(data)
        df.columns = columns
        #if numeric:
            #df[df.columns] = df[df.columns].apply(pd.to_numeric, errors="ignore")
        #if s_index:
            #df.set_index("Season", inplace=True)
        return df

def dict_to_np(dfDict, featureList):
    nFeatures   = len(featureList)
    npData      = []
    idList      = []
    for team in tools.teamList:
        df = dfDict[team]
        for season in tools.seasonList:
            seasonDf = df[df["Season"]==season]
            if not seasonDf.empty:
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





#
