import requests
import time

API_KEY = 'ae35a20f9c5e9701e61aae3c11a7aa82' #MINE

APIKEY = 'c6196c01e7c1d93932590f42beec9ef8'

url = f"https://apiclient.besoccerapps.com/scripts/api/api.php"

class Equip:
    def __init__(self, name):
        self.name = name
        self.victories = [0, 0]
        self.empats = [0, 0]
        self.derrotes = [0, 0]
        self.punts = [0, 0]
        self.goalsFavor = [0, 0]
        self.goalsEnContra = [0, 0]

    def set_punts_finals(self):
        self.punts[0] = self.victories[0] * 3 + self.empats[0]
        self.punts[1] = self.victories[1] * 3 + self.empats[1]

    def trate_match(self, isLocal, result):
        res1 = int(result[0])
        res2 = int(result[2])

        if isLocal:
            self.goalsFavor[0] += res1
            self.goalsEnContra[0] += res2

            if res1 == res2:
                self.empats[0] += 1
            elif res1 > res2:
                self.victories[0] += 1
            else:
                self.derrotes[0] += 1

        else:
            self.goalsFavor[1] += res2
            self.goalsEnContra[1] += res1

            if res1 == res2:
                self.empats[1] += 1
            elif res1 < res2:
                self.victories[1] += 1
            else:
                self.derrotes[1] += 1

    def print_data(self):
        self.set_punts_finals()

        print(f"\nEstadistiques de {self.name}:\n")
        print("{:<16} {:>6} {:>9} {:>6}".format("", "Local", "Visitant", "Total"))

        print("{:<16} {:>6} {:>9} {:>6}".format("Punts:", str(self.punts[0]), str(self.punts[1]), str(self.punts[0] + self.punts[1])))
        print("{:<16} {:>6} {:>9} {:>6}".format("Victories:", str(self.victories[0]), str(self.victories[1]),str(self.victories[0] + self.victories[1])))
        print("{:<16} {:>6} {:>9} {:>6}".format("Empats:", str(self.empats[0]), str(self.empats[1]), str(self.empats[0] + self.empats[1])))
        print("{:<16} {:>6} {:>9} {:>6}".format("Derrotes:", str(self.derrotes[0]), str(self.derrotes[1]), str(self.derrotes[0] + self.derrotes[1])))

        print("\n{:<16} {:>6} {:>9} {:>6}".format("Gols a favor:", str(self.goalsFavor[0]), str(self.goalsFavor[1]), str(self.goalsFavor[0] + self.goalsFavor[1])))
        print("{:<16} {:>6} {:>9} {:>6}".format("Gols en contra:", str(self.goalsEnContra[0]), str(self.goalsEnContra[1]), str(self.goalsEnContra[0] + self.goalsEnContra[1])))
        print("{:<16} {:>6} {:>9} {:>6}".format("Diferencia gols:", str(self.goalsFavor[0]-self.goalsEnContra[0]), str(self.goalsFavor[1]-self.goalsEnContra[1]), str(self.goalsFavor[0]-self.goalsEnContra[0] + self.goalsFavor[1] - self.goalsEnContra[1])))



def get_data(year, nom1, nom2):
    equip1 = Equip(nom1)
    equip2 = Equip(nom2)

    for jornada in range(1, 39):
        params = {
            'key': APIKEY,
            'format': 'json',
            'req': 'matchs',
            'league': '1',
            'tz': 'Europe/Madrid',
            'year': year,
            'round': jornada
        }

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload, params=params)
        data = response.json()

        partidos = data['match']


        for partido in partidos:
            local = partido['local']
            visitor = partido['visitor']
            result = partido['result']

            if local == nom1:
                equip1.trate_match(True, result)
            elif local == nom2:
                equip2.trate_match(True, result)

            if visitor == nom1:
                equip1.trate_match(False, result)
            elif visitor == nom2:
                equip2.trate_match(False, result)

            if local == nom1 and visitor == nom2 or local == nom2 and visitor == nom1:
                estadio = partido['stadium']
                print(f"Jornada {jornada}: {local} vs {visitor} - Resultado: {result} - Estadio: {estadio}")

    equip1.print_data()
    equip2.print_data()


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










