import requests
import time

API_KEYM = 'ae35a20f9c5e9701e61aae3c11a7aa82' #MINE

APIKEY = 'c6196c01e7c1d93932590f42beec9ef8'
APIKEY2= 'b3fcd6725e03f4e5d588f6624cac5522'

API_KEY = 'c6196c01e7c1d93932590f42beec9ef8'  # Consolidated single API key
BASE_URL = "https://apiclient.besoccerapps.com/scripts/api/api.php"

class TeamStats:
    def __init__(self, name):
        self.name = name
        self.stats = {
            'local': {'victories': 0, 'draws': 0, 'defeats': 0, 'goals_for': 0, 'goals_against': 0},
            'visitor': {'victories': 0, 'draws': 0, 'defeats': 0, 'goals_for': 0, 'goals_against': 0}
        }

    def update_match(self, is_home, result):
        home_goals, away_goals = map(int, result.split('-'))
        side = 'local' if is_home else 'visitor'
        other_side = 'visitor' if is_home else 'local'

        self.stats[side]['goals_for'] += home_goals
        self.stats[side]['goals_against'] += away_goals

        if home_goals == away_goals:
            self.stats[side]['draws'] += 1
        elif home_goals > away_goals:
            if is_home:
                self.stats[side]['victories'] += 1
            else:
                self.stats[side]['defeats'] += 1
        else:
            if is_home:
                self.stats[side]['defeats'] += 1
            else:
                self.stats[side]['victories'] += 1

    def calculate_points(self, side):
        return self.stats[side]['victories'] * 3 + self.stats[side]['draws']

    def print_stats(self):
        print(f"\nStatistics for {self.name}:\n")
        print("{:<16} {:>6} {:>9} {:>6}".format("", "Local", "Visitor", "Total"))
        stats_fields = ['victories', 'draws', 'defeats', 'goals_for', 'goals_against']
        for field in stats_fields:
            local = self.stats['local'][field]
            visitor = self.stats['visitor'][field]
            total = local + visitor
            print("{:<16} {:>6} {:>9} {:>6}".format(field.capitalize() + ":", local, visitor, total))
        print("{:<16} {:>6} {:>9} {:>6}".format("Points:", self.calculate_points('local'), self.calculate_points('visitor'), self.calculate_points('local') + self.calculate_points('visitor')))

def get_data(year, team1, team2):
    team_stats1 = TeamStats(team1)
    team_stats2 = TeamStats(team2)

    session = requests.Session()  # Use session for connection pooling
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

        for match in matches:
            if match['local'] in (team1, team2) or match['visitor'] in (team1, team2):
                if match['local'] == team1:
                    team_stats1.update_match(True, match['result'])
                elif match['local'] == team2:
                    team_stats2.update_match(True, match['result'])
                if match['visitor'] == team1:
                    team_stats1.update_match(False, match['result'])
                elif match['visitor'] == team2:
                    team_stats2.update_match(False, match['result'])

                if (match['local'], match['visitor']) in [(team1, team2), (team2, team1)]:
                    print(f"Round {round_num}: {match['local']} vs {match['visitor']} - Result: {match['result']} - Stadium: {match['stadium']}")

    team_stats1.print_stats()
    team_stats2.print_stats()
    session.close()

if __name__ == '__main__':
    inicio = time.time()
    #year = input("Year: ")
    #nom_equip1 = input("Nombre del equipo 1: ")
    #nom_equip2 = input("Nombre del equipo 2: ")

    year = '2023'
    nom_equip1 = 'Barcelona'
    nom_equip2 = 'Real Madrid'
    get_data(year, nom_equip1, nom_equip2)

    fin = time.time()
    duracion = fin - inicio
    print(f"\nEl tiempo de ejecución fue de {duracion} segundos")










