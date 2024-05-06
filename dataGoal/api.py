import requests
import time
import matplotlib.pyplot as plt
import random

API_KEYM = 'ae35a20f9c5e9701e61aae3c11a7aa82'  # MINE

APIKEY2 = 'b3fcd6725e03f4e5d588f6624cac5522'

API_KEY = 'c6196c01e7c1d93932590f42beec9ef8'  # Consolidated single API key
BASE_URL = "https://apiclient.besoccerapps.com/scripts/api/api.php"


class Year:
    def __init__(self, title, year):
        self.title = title
        self.year = year


class TeamStats:
    def __init__(self, name):
        self.name = name
        self.stats = {
            'local': {'victories': 0, 'draws': 0, 'defeats': 0, 'goals_for': 0, 'goals_against': 0, 'goal_diff': 0, 'points': 0},
            'visitor': {'victories': 0, 'draws': 0, 'defeats': 0, 'goals_for': 0, 'goals_against': 0, 'goal_diff': 0, 'points': 0},
        }
        self.abreviation = ""
        self.estadi = ""
        self.escut_url = ""

    def update_info(self, abr, est, url):
        self.abreviation = abr
        self.estadi = est
        self.escut_url = url
    def update_match(self, is_home, result):
        home_goals, away_goals = map(int, result.split('-'))
        if is_home:
            self.stats['local']['goals_for'] += home_goals
            self.stats['local']['goals_against'] += away_goals
            if home_goals == away_goals:
                self.stats['local']['draws'] += 1
            elif home_goals > away_goals:
                self.stats['local']['victories'] += 1
            else:
                self.stats['local']['defeats'] += 1
        else:
            self.stats['visitor']['goals_for'] += away_goals
            self.stats['visitor']['goals_against'] += home_goals
            if home_goals == away_goals:
                self.stats['visitor']['draws'] += 1
            elif home_goals < away_goals:
                self.stats['visitor']['victories'] += 1
            else:
                self.stats['visitor']['defeats'] += 1

    def calculate_points(self):
        self.stats['local']['points'] = self.stats['local']['victories']*3 + self.stats['local']['draws']
        self.stats['visitor']['points'] = self.stats['visitor']['victories']*3 + self.stats['visitor']['draws']

    def calculate_goal_difference(self):
        self.stats['local']['goal_diff'] = self.stats['local']['goals_for'] - self.stats['local']['goals_against']
        self.stats['visitor']['goal_diff'] = self.stats['visitor']['goals_for'] - self.stats['visitor']['goals_against']


def get_years():
    session = requests.Session()
    params = {
        'key': API_KEY,
        'format': 'json',
        'req': 'seasons',
        'tz': 'Europe/Madrid',
        'id': '1'
    }

    response = session.get(BASE_URL, params=params)
    seasons = response.json()['seasons']

    return seasons[0:5]


def get_teams(year):
    session2 = requests.Session()
    result = []
    params = {
        'key': API_KEY,
        'format': 'json',
        'req': 'tables',
        'league': '1',
        'tz': 'Europe/Madrid',
        'year': year
    }

    response = session2.get(BASE_URL, params=params)
    teams = response.json()['table']
    for team in teams:
        result.append(team['team'])

    result.sort()
    return result

def get_teams_without_selected(teams, selected_team):
    filtered_teams = {team for team in teams if team != selected_team}
    sorted_teams = sorted(filtered_teams)
    return sorted_teams


def get_data(year, team1, team2):
    session = requests.Session()
    team_stats1 = TeamStats(team1)
    team_stats2 = TeamStats(team2)

    for round_num in range(1, 39):
        params = {
            'key': API_KEY,
            'format': 'json',
            'req': 'matchs',
            'league': '1',
            'tz': 'Europe/Madrid',
            'year': year,
            'round': round_num
        }

        response = session.get(BASE_URL, params=params)
        matches = response.json()['match']
        inicial1 = True
        inicial2 = True


        for match in matches:

            if match['result'] == "x-x":  # Partit no jugat
                continue
            if match['local'] in (team1, team2) or match['visitor'] in (team1, team2):
                if (match['local'], match['visitor']) in [(team1, team2), (team2, team1)]:
                    print(
                        f"Round {round_num}: {match['local']} vs {match['visitor']} - Result: {match['result']} - Stadium: {match['stadium']}")

                if match['local'] == team1:
                    if inicial1 == True:
                        team_stats1.update_info(match['local_abbr'], match['stadium'], match['local_shield'])
                        inicial1 = False
                    team_stats1.update_match(True, match['result'])

                elif match['local'] == team2:
                    if inicial2 == True:
                        team_stats2.update_info(match['local_abbr'], match['stadium'], match['local_shield'])
                        inicial2 = False
                    team_stats2.update_match(True, match['result'])

                if match['visitor'] == team1:
                    team_stats1.update_match(False, match['result'])
                elif match['visitor'] == team2:
                    team_stats2.update_match(False, match['result'])

    team_stats1.calculate_points()
    team_stats2.calculate_points()

    team_stats1.calculate_goal_difference()
    team_stats2.calculate_goal_difference()


    return team_stats1, team_stats2


def get_example():
    session = requests.Session()
    round_num = 1
    year = 2023
    params = {
        'key': API_KEY,
        'format': 'json',
        'req': 'matchs',
        'league': '1',
        'tz': 'Europe/Madrid',
        'year': year,
        'round': round_num
    }

    response = session.get(BASE_URL, params=params)
    matches = response.json()['match']
    return matches


if __name__ == '__main__':
    global session

    inicio = time.time()

    session = requests.Session()  # Use session for connection pooling

    years = get_years()

    numero_aleatorio2 = random.randint(0, len(years) - 1)
    year = years[numero_aleatorio2]

    print(f"\n\nTitle: {year.title} \t YEAR: {year.year}")

    noms_equips, positions = get_teams(year.year)

    numero_aleatorio3 = random.randint(0, len(noms_equips) - 1)
    print("Nom equip 1: \t" + noms_equips[numero_aleatorio3])

    numero_aleatorio4 = numero_aleatorio3

    while (numero_aleatorio4 == numero_aleatorio3):
        numero_aleatorio4 = random.randint(0, len(noms_equips) - 1)

    print("Nom equip 2: \t" + noms_equips[numero_aleatorio4])

    get_data(year.year, noms_equips[numero_aleatorio3],
             noms_equips[numero_aleatorio4], positions[numero_aleatorio3], positions[numero_aleatorio4])

    fin = time.time()
    duracion = fin - inicio
    print(f"\nEl tiempo de ejecución fue de {duracion} segundos")
