import numpy as np
import os
import sys
import pandas as pd
import tools
import requests
from bs4 import BeautifulSoup
sys.path.append('../python/')
import tools
################################################################################
BASE_URL = "https://www.basketball-reference.com"
################################################################################
def scrape_all_teams(teamList, verbose=False):
    dfDict = {}
    for team in teamList:
    	if verbose: print(team)
    	dfDict[team] = get_team_stats_basic(team)
    print("first few rows of an example data frame:")
    print(dfDict["CLE"][0:5])
    return dfDict
################################################################################
def scrape_player_names(season=2019):
    '''
    Srapes bball ref and returns a list of player names (with no special formatting)
    for all players active in the given season.
    '''
    url = BASE_URL + "/leagues/NBA_" + str(season) + "_per_game.html"
    r = requests.get(url)
    if r.status_code == 404:
        print("page not found")
    else:
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll("table")
        if len(tables) == 1: table = tables[0]
        else:
            print("More than one table found, don't know what to do")
            print(tables)
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
        playerNameList = df['Player'].values
        return playerNameList
################################################################################
def get_player_stats_basic(player):
    '''
    Takes a player lookup string and scrapes thier basic stats table from
    bball ref.  Returns a pandas data frame with each row being a season's stats.
    '''
    url = BASE_URL + "/players/" + player[:1] + "/" + player + ".html"
    r = requests.get(url)
    if r.status_code == 404:
        print("page not found")
    else:
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll("table")
        print(tables)
        if len(tables) == 1: table = tables[0]
        #elif len(tables)>1:
            #print("More than one table found, don't know what to do")
            #print(tables)
        #elif len(tables)<1:
            #print("Table not found")
            #print(tables)
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
        df.name    = player
        #if numeric:
            #df[df.columns] = df[df.columns].apply(pd.to_numeric, errors="ignore")
        #if s_index:
            #df.set_index("Season", inplace=True)
        return df
################################################################################
def get_team_stats_basic(team):
    '''
    Takes a team abbreviation and scrapes that team's stats table for
    year end stats for each season.  Returns a pandas data frame.
    '''
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




#
