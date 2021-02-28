import os
import random
import texttable
from sys import platform

class Game:

    def __init__(self, teams):
        self.teams = teams
        self.TEAM_SIZE = len(self.teams[0])

        self.innings = 9
        self.hits = ["singles", "doubles", "triples", "homes"]

        self.flip = lambda: random.choice([True, False])
        self.chance = lambda p: (False, True)[random.random() < p]

        for i in range(len(self.teams)):
            if len(self.teams[i]) != self.TEAM_SIZE:
                print("Please input a teams array with the correct amount of players!")
                exit(1)

    def dump(self, statType):
        makeshift, out = [], []

        exec_string = "player_list.append(self.teams[{}][{}].{})"
        for i in range(len(self.teams)):
            player_list = []
            for j in range(len(self.teams[i])):
                run_str = exec_string.format(i, j, statType)
                exec(run_str)
            makeshift.append(player_list)

        # print(f"STATS: {makeshift}")
        return makeshift

    def play(self):
        for i in range(0, self.innings + 1):
            outs = 0
            while outs < 6:
                if self.flip():
                    self.hit()
                else:
                    outs += 1

    def hit(self):
        for i in range(len(self.teams)):
            hitType = random.choice(self.hits)

            scored = {
                "singles": self.chance(0.10),
                "doubles": self.chance(0.20),
                "triples": self.chance(0.50),
                "homes": True
            }
            random.choice(self.teams[i]).recordHit(hitType, scored[hitType])


class Player:

    def __init__(self, fName, lName):
        self.firstName = fName
        self.lastName = lName

        self.hits = {
            "singles": 0,
            "doubles": 0,
            "triples": 0,
            "homes": 0
        }

        self.runs = {
            "singles": 0,
            "doubles": 0,
            "triples": 0,
            "homes": 0
        }

        self.total = {
            "hits": 0,
            "runs": 0
        }

        self.percentage = 0

        self.update()

    def recordHit(self, hitType, runnerScored):
        self.hits[hitType] += 1
        if runnerScored: self.runs[hitType] += 1

        self.update()

    def scoringPercentage(self):

        if self.total["runs"] > 0:
            return round((self.total["runs"] / self.total["hits"]) * 100, 2)
        else:
            return "N/A"

    def update(self):
        hitNum, runNum = 0, 0

        for value in self.hits.values():
            hitNum += value
        for value in self.runs.values():
            runNum += value

        self.total["hits"] = hitNum
        self.total["runs"] = runNum

        self.percentage = self.scoringPercentage()

        return 0


def main():

    teams = []
    TEAM_SIZE = 9
    first, last = [], []

    textfile_directory = os.path.join(os.path.join(os.pardir, os.getcwd()), "txt") if platform != "darwin" else "../txt"

    files = {
        "first": "firstnames.txt",
        "last": "lastnames.txt"
    }

    for key in files:
        path = os.path.join(textfile_directory, files[key])
        arr = []

        with open(path, "r") as f:
            for lines in f:
                arr.append(lines.rstrip())

        random.shuffle(arr)
        files[key] = arr[:(TEAM_SIZE * 2)]

    # print(f"FIRST: {files['first']}")
    # print(f"LAST: {files['last']}")

    k = 0
    for i in range(0, 2):
        player_list = []
        for j in range(TEAM_SIZE):
            player_list.append(Player(files["first"][k], files["last"][k]))
            k += 1
        teams.append(player_list)

    game = Game(teams)
    game.play()

    table = texttable.Texttable()
    table.set_cols_align(["c", "c", "c", "c", "c"])
    table.add_row(["Last", "First", "Hits", "Runs", "Percentage"])
    # f'{round(float(game.dump("percentage")[i][j]), 2)}%'
    # game.dump("percentage")[i][j]
    for i in range(len(game.teams)):
        for j in range(len(game.dump("firstName")[i])):
            percentage = game.dump("percentage")[i][j]
            table.add_row([game.dump("lastName")[i][j], game.dump("firstName")[i][j], game.dump("total['hits']")[i][j], game.dump("total['runs']")[i][j], percentage if isinstance(percentage, str) else f'{round(float(percentage), 2)}%'])

    main = table.draw()

    table = texttable.Texttable()
    table.set_cols_align(["c", "c", "c", "c", "c", "c"])
    table.add_row(["Last", "Singles", "Doubles", "Triples", "Homers", "Percentage"])

    for i in range(len(game.teams)):
        for j in range(len(game.dump("firstName")[i])):
            percentage = game.dump("percentage")[i][j]
            table.add_row([game.dump("lastName")[i][j], game.dump("hits['singles']")[i][j], game.dump("hits['doubles']")[i][j], game.dump("hits['triples']")[i][j], game.dump("hits['homes']")[i][j], percentage if isinstance(percentage, str) else f'{round(float(percentage), 2)}%'])

    stats = table.draw()

    table = texttable.Texttable()
    table.set_cols_align(["c", "c", "c", "c", "c", "c", "c", "c"])
    table.add_row(["Name", "Singles", "Doubles", "Triples", "Homers", "Hits", "Runs", "Percentage"])

    for i in range(len(game.teams)):
        for j in range(len(game.dump("firstName")[i])):
            percentage = game.dump("percentage")[i][j]
            table.add_row([f'{game.dump("lastName")[i][j]}, {game.dump("firstName")[i][j]}', game.dump("hits['singles']")[i][j], game.dump("hits['doubles']")[i][j], game.dump("hits['triples']")[i][j], game.dump("hits['homes']")[i][j], game.dump("total['hits']")[i][j], game.dump("total['runs']")[i][j], percentage if isinstance(percentage, str) else f'{round(float(percentage), 2)}%'])

    full = table.draw()

    # print(main)
    # print(stats)
    print(full)



if __name__ == '__main__':
    main()
