import pandas as pd
import requests
from enum import Enum

class Teams(Enum):
    TAPPARA = "Tappara"
    ILVES = "Ilves"
    KÄRPÄT = "Kärpät"
    HIFK = "HIFK"
    JYP = "JYP"
    LUKKO = "Lukko"
    TPS = "TPS"
    SAIPA = "SaiPa"
    PELICANS = "Pelicans"
    KALPA = "KalPa"
    ÄSSÄT = "Ässät"
    JUKURIT = "Jukurit"
    HPK = "HPK"
    KOOKOO = "KooKoo"
    SPORT = "Sport"

matches_data = requests.get('https://www.liiga.fi/api/v1/games?tournament').json()

teams_data = requests.get('https://liiga.fi/api/v1/teams/stats/2024/runkosarja/').json()

df = pd.DataFrame(matches_data)

df_teams = pd.DataFrame(teams_data)

endedGamesDf = df.drop(df.index[df['ended'] == False])

xGtable = pd.DataFrame(columns=['Joukkue',
        'G',
        'xG',
        'G - xG',
        'GA', 
        'xGA',
        'xGA - GA'])

def teamData(team, home, data):
    array = []
    for indeksi, rivi in endedGamesDf.iterrows():
            if home == True and rivi['homeTeam']['teamName'] == team:
                array.append(rivi['homeTeam'][data])
            elif home == False and rivi['awayTeam']['teamName'] == team:
                array.append(rivi['awayTeam'][data])
    return array

def getTeamOpponentData(team, home, data):
    array = []
    for indeksi, rivi in endedGamesDf.iterrows():
            if home == True and rivi['homeTeam']['teamName'] == team:
                array.append(rivi['awayTeam'][data])
            elif home == False and rivi['awayTeam']['teamName'] == team:
                array.append(rivi['homeTeam'][data])
    return array

def addData(team):
    goals = sum(teamData(team, True, 'goals')) + sum(teamData(team, False, 'goals'))
    goalsAgainst = sum(getTeamOpponentData(team, True, 'goals')) + sum(getTeamOpponentData(team, False, 'goals'))
    exceptedGoals = sum(teamData(team, True, 'expectedGoals')) + sum(teamData(team, False, 'expectedGoals'))
    exceptedGoalsAgainst = sum(getTeamOpponentData(team, True, 'expectedGoals')) + sum(getTeamOpponentData(team, False, 'expectedGoals'))
    newData = pd.DataFrame({
        'Joukkue': [team],
        'G':[goals],
        'xG': exceptedGoals,
        'G - xG': [round(goals - exceptedGoals,2)],
        'GA': [goalsAgainst], 
        'xGA': [exceptedGoalsAgainst],
        'xGA - GA': [round(exceptedGoalsAgainst - goalsAgainst,2)],
        'xGD': [round(goals - exceptedGoals,2) + round(exceptedGoalsAgainst - goalsAgainst,2)],
        'PDO': [getTeamDataFromDf(team,'pdo')],
        'CORSI%': [getTeamDataFromDf(team, 'corsi_percentage')] 
        })
    return newData

def addTeamsToxGtable():
    xGtable = pd.DataFrame()
    for team in Teams:
        xGtable = pd.concat([xGtable,addData(team.value)],ignore_index=True)
    print(xGtable)
    
def getTeamDataFromDf(team, data):
    teamAsLowercase = team.lower()
    teamWithoutÄÖ = teamAsLowercase.replace('ä','a').replace('ö','o')
    for i, rivi in df_teams.iterrows():
        if rivi['slug'] == teamWithoutÄÖ:
            return rivi[data]

def compareTeams(team1, team2):
    compareTable = pd.DataFrame()
    compareTable = pd.concat([addData(team1),addData(team2)])
    print(compareTable)

addTeamsToxGtable()
compareTeams('TPS','HIFK')