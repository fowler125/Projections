from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime,date

games_url = 'https://www.teamrankings.com/nba/schedules/'

first_half_url = 'https://www.teamrankings.com/nba/stat/1st-half-points-per-game'

Teams = {}

now = datetime.now()
today = date.today()
d4 = today.strftime("%b-%d-%Y")

def FirstHalfStats():
    html = urlopen(first_half_url)
    stats_page = BeautifulSoup(html,'html.parser')

    stats_chart = stats_page.find("tbody")

    stat_per_team = stats_page.find_all("tr")

    #print(stats_chart)
    y = stat_per_team.__len__()
    i = 1
    for stat_per_teams in stat_per_team:

        if (i < y):
            team_name = stat_per_team[i].find("a").text.strip()
            team_stats_2022 = stat_per_team[i].contents[5].text.strip()
            team_stats_last3 = stat_per_team[i].contents[7].text.strip()
            team_stats_last1 = stat_per_team[i].contents[9].text.strip()
            team_stats_Home = stat_per_team[i].contents[11].text.strip()
            team_stats_Away = stat_per_team[i].contents[13].text.strip()
            team_stats_2021 = stat_per_team[i].contents[15].text.strip()


            Teams[i] = {}
            Teams[i]['Team'] = team_name
            Teams[i]['2022'] = team_stats_2022
            Teams[i]['Last 3'] = team_stats_last3
            Teams[i]['Last 1'] = team_stats_last1
            Teams[i]['Home'] = team_stats_Home
            Teams[i]['Away'] = team_stats_Away
            Teams[i]['2021'] = team_stats_2021

            i = i + 1

    #print(Teams)

def GameMatchups():
    f = open(f"Matchups/{d4}.txt","w+")
    html = urlopen(games_url)
    games_page = BeautifulSoup(html, 'html.parser')

    game_chart = games_page.find(id="content")

    team_stats = games_page.find_all("tr")
    matchups = []
    regex = r"[a-zA-Z]+"

    y = team_stats.__len__()
    i = 1
    for team_stat in team_stats:

        if(i < y):
            team_matchup = team_stats[i].find("a").text.strip()

            i = i+1
            test_str = team_matchup
            pattern = r'[0-9]|\#'

            new_string = re.sub(pattern,'',test_str)
            ReformatString(new_string)

            f.writelines(f"{new_string}\n")

def ReformatString(string):
    query = string
    stopwords = {'what','who','is','a','at','is','he',''}

    resultwords = [word for word in re.split("\W+", query) if word.lower() not in stopwords]

    prewords = {'New','Golden','LA','Okla','San'}

    if resultwords[0] in prewords:
        resultwords[0] = resultwords[0] + ' ' + resultwords[1]
        resultwords.remove(resultwords[1])
    if resultwords[1] in prewords:
        resultwords[1] = resultwords[1] + ' ' + resultwords[2]
        resultwords.remove(resultwords[2])

    DisplayStats(Teams,resultwords[0],resultwords[1])
    return (resultwords)

def DisplayStats(list,team1,team2):
    #print('-------------------------------------------------------------')
    list1 = []
    list2 = []
    list_total = []
    labels = ['2022', 'Last 3', 'Last 1', 'Home', 'Away', '2021']

    for team_id, team_info in list.items():
        #print("\nteam_id:", team_id)

        for key in team_info:
            if team_info[key] == team1:
                for key in team_info:
                    #print(key+': '+team_info[key])
                    list1.append(team_info[key])

        for key in team_info:
            if team_info[key] == team2:
                for key in team_info:
                    #print(key+': '+team_info[key])
                    list2.append(team_info[key])

    #print(f'--------------------- Totals {list1[0]} v. {list2[0]} -----------------------')
    FirstTeam = list1[0]
    SecondTeam = list2[0]
    list1.remove(list1[0])
    list2.remove(list2[0])

    pointer = 0

    for i in list1:

        label = labels[pointer]
        temp = float(list1[pointer])
        temp2 = float(list2[pointer])
        temp_total = temp + temp2
        #print(f"Total {label}: {temp_total}")
        temp_total = ('%.2f' % temp_total)
        list_total.append(temp_total)

        pointer = pointer + 1
    GridBuilder(FirstTeam,SecondTeam, list1, list2, list_total)


def GridBuilder(TeamOneName,TeamNameTwo,team_one,team_two,team_total):
    print(f"-------------- {TeamOneName} v. {TeamNameTwo} --------------------")
    labels = ['2022', 'Last 3', 'Last 1', 'Home', 'Away', '2021']
    for label in labels:
        print(f'{label}', end='     ')
    print('\n')
    for stat in team_one:
        print(f'{stat}', end='      ')
    print(TeamOneName)
    print('\n')
    for stat in team_two:
        print(f'{stat}', end='      ')
    print(TeamNameTwo)
    print('\n')
    for stat in team_total:
        print(f'{stat}', end='    ')
    print('Totals')
    print('\n')


def Combination():
    FirstHalfStats()
    GameMatchups()

if __name__ == '__combination__':
    Combination()
