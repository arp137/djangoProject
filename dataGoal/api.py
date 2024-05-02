import requests
import time
import matplotlib.pyplot as plt
import random

API_KEYM = 'ae35a20f9c5e9701e61aae3c11a7aa82'  # MINE

APIKEY2 = 'b3fcd6725e03f4e5d588f6624cac5522'

API_KEY = 'c6196c01e7c1d93932590f42beec9ef8'  # Consolidated single API key
BASE_URL = "https://apiclient.besoccerapps.com/scripts/api/api.php"


class Category:
    def __init__(self, id, league_id, name, num_rounds):
        self.id = id
        self.league_id = league_id
        self.name = name
        self.num_rounds = num_rounds


class Year:
    def __init__(self, title, year):
        self.title = title
        self.year = year


class TeamStats:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.stats = {
            'local': {'victories': 0, 'draws': 0, 'defeats': 0, 'goals_for': 0, 'goals_against': 0},
            'visitor': {'victories': 0, 'draws': 0, 'defeats': 0, 'goals_for': 0, 'goals_against': 0}
        }

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

    def calculate_points(self, side):
        return self.stats[side]['victories'] * 3 + self.stats[side]['draws']

    def calculate_goal_difference(self, side):
        return self.stats[side]['goals_for'] - self.stats[side]['goals_against']

    def print_stats(self):
        print(f"\nStatistics for {self.name} (Position {self.position}):\n")
        print("{:<16} {:>6} {:>9} {:>6}".format("", "Local", "Visitor", "Total"))
        stats_fields = ['victories', 'draws', 'defeats', 'goals_for', 'goals_against', 'goal_difference']
        for field in stats_fields[:-1]:
            local = self.stats['local'][field]
            visitor = self.stats['visitor'][field]
            total = local + visitor
            print("{:<16} {:>6} {:>9} {:>6}".format(field.capitalize() + ":", local, visitor, total))
        # Print goal differences separately
        local_diff = self.calculate_goal_difference('local')
        visitor_diff = self.calculate_goal_difference('visitor')
        total_diff = local_diff + visitor_diff
        print("{:<16} {:>6} {:>9} {:>6}".format("Goal Difference:", local_diff, visitor_diff, total_diff))
        print("{:<16} {:>6} {:>9} {:>6}".format("Points:", self.calculate_points('local'),
                                                self.calculate_points('visitor'),
                                                self.calculate_points('local') + self.calculate_points('visitor')))

    def plot_stats(self):
        categories = ['victories', 'draws', 'defeats', 'goals_for', 'goals_against']
        local_values = [self.stats['local'][key] for key in categories]
        visitor_values = [self.stats['visitor'][key] for key in categories]

        x = list(range(len(categories)))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar([xi - width / 2 for xi in x], local_values, width, label='Local')
        rects2 = ax.bar([xi + width / 2 for xi in x], visitor_values, width, label='Visitor')

        ax.set_ylabel('Count')
        ax.set_title(f'Stats by category for {self.name}')
        ax.set_xticks(x)
        ax.set_xticklabels(['Victories', 'Draws', 'Defeats', 'Goals For', 'Goals Against'])
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        plt.show()



def get_years(league_id):
    years = []
    params = {
        'key': API_KEY,
        'format': 'json',
        'req': 'seasons',
        'tz': 'Europe/Madrid',
        'id': league_id
    }

    response = session.get(BASE_URL, params=params)
    print(response.json())
    seasons = response.json()['seasons']

    print(seasons)

    for index, season in enumerate(seasons):
        if index >= 5:
            break
        cur_year = Year(season['title'], season['year'])
        years.append(cur_year)

    return years


def get_teams(year):
    session2 = requests.Session()
    result = []
    positions = []
    params = {
        'key': API_KEY,
        'format': 'json',
        'req': 'tables',
        'league': league_id,
        'tz': 'Europe/Madrid',
        'year': year
    }

    response = session2.get(BASE_URL, params=params)
    teams = response.json()['table']
    for team in teams:
        result.append(team['team'])
        positions.append(team['pos'])

    return result, positions


def get_data(year, team1, team2, pos1, pos2):
    team_stats1 = TeamStats(team1, pos1)
    team_stats2 = TeamStats(team2, pos2)

    for round_num in range(1, 39):
        params = {
            'key': API_KEY,
            'format': 'json',
            'req': 'matchs',
            'league': league_id,
            'tz': 'Europe/Madrid',
            'year': year,
            'round': round_num
        }

        response = session.get(BASE_URL, params=params)
        matches = response.json()['match']

        for match in matches:
            if match['result'] == "x-x":  # Partit no jugat
                continue
            if match['local'] in (team1, team2) or match['visitor'] in (team1, team2):
                if (match['local'], match['visitor']) in [(team1, team2), (team2, team1)]:
                    print(
                        f"Round {round_num}: {match['local']} vs {match['visitor']} - Result: {match['result']} - Stadium: {match['stadium']}")

                if match['local'] == team1:
                    team_stats1.update_match(True, match['result'])
                elif match['local'] == team2:
                    team_stats2.update_match(True, match['result'])

                if match['visitor'] == team1:
                    team_stats1.update_match(False, match['result'])
                elif match['visitor'] == team2:
                    team_stats2.update_match(False, match['result'])

    team_stats1.print_stats()
    team_stats2.print_stats()
    team_stats1.plot_stats()
    team_stats2.plot_stats()
    session.close()


def get_example():
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

    years = get_years(category.id)

    numero_aleatorio2 = random.randint(0, len(years) - 1)
    year = years[numero_aleatorio2]

    print(f"\n\nTitle: {year.title} \t YEAR: {year.year}")

    noms_equips, positions = get_teams(category.id, year.year)

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

API_KEY_DAVID = "fc4c9ad17ff8445f98d75b0653762d6e"


def get_teams2():
    url = f'https://api.football-data.org/v4/competitions/PD/teams'
    headers = {'X-Auth-Token': API_KEY_DAVID}
    response = requests.get(url, headers=headers)
    return response.json()


def get_equip_info(equip_id):
    base_url = 'https://api.football-data.org/v4/'
    end_point = f'teams/{equip_id}'
    headers = {'X-Auth-Token': API_KEY_DAVID}
    response = requests.get(base_url + end_point, headers=headers)
    return response.json()
