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

response = requests.get('https://www.liiga.fi/api/v1/games?tournament')

data = response.json()

df = pd.DataFrame(data)

endedGamesDf = df.drop(df.index[df['ended'] == False])

xGtable = pd.DataFrame(columns=['Joukkue',
        'G',
        'xG',
        'G - xG',
        'GA', 
        'xGA',
        'GA - xGA'])

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
        'GA - xGA': [round(goalsAgainst - exceptedGoalsAgainst,2)]
        })
    return newData

def addTeamsToxGtable():
    xGtable = pd.DataFrame()
    for team in Teams:
        xGtable = pd.concat([xGtable,addData(team.value)],ignore_index=True)
    print(xGtable)

addTeamsToxGtable()