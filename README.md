<h1><center> Game-n-Score </h1></center>

<body style="background-color:#292C34"></body>

<center><i> A simple project to parse randomized data of sport statistics. </i></center>

<br></br>

***This documentation should aid in the comprehsion in this case of this being digested in such a medium, making for a smooth transition and easy pick-up from what is already provided.***

### Dependencies

- [Poetry](https://github.com/python-poetry/poetry)
    - **Linux**
    ```sh
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
    ```
    - **Windows**
    ```powershell
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python3 -
    ```
    - **Or (Python)**
    ```sh
    python3 -m pip install poetry
    ```
## ***Classes***
 - Modulated classes for easy serilization and/or importing as a dependancy. 
    - For this reason, please resort to doing this rather than calling the `main()` function as a standalone.
1. ### Game

    ```python
    class Game:
        def __init__(self, teams):
            self.teams = teams
    ```
    *Declaring local class variables imported from the defintion made on each creation...*
    ```python
            self.TEAM_SIZE = len(self.teams[0])
    ```
    *Allowing for the customization of the the `TEAM_SIZE` variable.*
    ```python
            self.innings = 9
    ```
    *Setting the default innings to **nine** as this parameter should not generally be changed...*
    ```python
            self.hits = ["singles", "doubles", "triples", "homes"]
    ```
    *Defining types of hits that could be found; creating a dictionary.*

    ```python
            self.flip = lambda: random.choice([True, False])
            self.chance = lambda p: (False, True)[random.random() < p]
    ```
    *Creation of two anonymous lambda function to caculate chance; later to be used in the generation of the statistics.*

    ```python
            for i in range(len(self.teams)):
                if len(self.teams[i]) != self.TEAM_SIZE:
                        print("Please input a teams array with the correct amount of players!")
                        exit(1)
    ```
    *Checking the each team has the correct amount of players, using the given `TEAM_SIZE` variable.*

    ```python
        def dump(self, statType):
            makeshift, out = [], []
    ```
    *Declaring two temporary arrays to be used in the processing of the `teams` array.*

    ```python
            exec_string = "player_list.append(self.teams[{}][{}].{})"
                for i in range(len(self.teams)):
                    player_list = []
    ```
    *Cycling through the `teams` array with the `i` index. Template `exec_string` to specifically grab a certain property from each `player`.*
    ```python
                    for j in range(len(self.teams[i])):
                        run_str = exec_string.format(i, j, statType)
                        exec(run_str)
                    makeshift.append(player_list)
    ```
    *Cycling through each `player` in the `teams` array with the `j` index. Each `player` with have the input string, `statType` extracted from them, appended to the `makeshift` array.*

    ***(Comment: Please don't hurt me for using exec() in 2021. I just did it for the high amounts of customizability and extensibility. Much luv <3)***
    ```python
            return makeshift
    ```
    *Returning the concatenated array of `player` properties on a per-team basis.*

    ```python
        def play(self):
            for i in range(0, self.innings + 1):
    ```
    *Very basic cycle to replicate the effect of running through the pre-determined amount of `innings`.*

    ```python
                outs = 0
                while outs < 6:
                    if self.flip():
                        self.hit()
    ```
    *Running our class's `hit()` function on the probabilty of a coin-flip. This is how we replicate a real ball-game.*

    ```python
                    else:
                        outs += 1
    ```
    *The simple other end of the flip, causing the outs of the given hitter to be incremented.*

    ```python
        def hit(self):
            for i in range(len(self.teams)):
                hitType = random.choice(self.hits)
    ```
    *If called from the `play()` function, a random `hitType` will be assigned while cycling through `teams`.*

    ```python
                scored = {
                            "singles": self.chance(0.10),
                            "doubles": self.chance(0.20),
                            "triples": self.chance(0.50),
                            "homes": True
                }
                random.choice(self.teams[i]).recordHit(hitType, scored[hitType])
    ```    
    *With each `hitType` that is defined, a proportional chance of scoring is assigned, then randomly given to a player on the given team in `i`.*

2. ### Player

    ```python
    class Player:
        def __init__(self, fName, lName):
    ```
    *New class declaration taking in a `fName` and `lName` to build the `Player` persona.*

    ```python
            self.hits = {
                "singles": 0,
                "doubles": 0,
                "triples": 0,
                "homes": 0
            }
    ```
    *The definition of `hits` that a `Player` can make, stored for each individual instance of a `teams[i]`.*

    ```python
            self.runs = {
                "singles": 0,
                "doubles": 0,
                "triples": 0,
                "homes": 0
            }
    ```
    *While ignoring the fact this could be done in a single dictionary with corrisponding nested properties, we will say this repetition is for the sake of verbosity and readability.*

    ```python
            self.total = {
                "hits": 0,
                "runs": 0
            }
    ```
    *Once again an instanciation of a `total` dictiory for the simple purpose of easy-access for future statistics manipulation.*

    ```python
            self.percentage = 0

            self.update()
    ```
    *Declaring easy-access to a `percentage` variable, and calling the built-in `update()` function on \_\_init\_\_.*

    ```python
        def recordHit(self, hitType, runnerScored):
            self.hits[hitType] += 1
    ```
    *Taking in two parameters, `hitType` & `runnerScored`, incrementing our `hits[...]` with the `hitType` parameter.*

    ```python
            if runnerScored: self.runs[hitType] += 1

            self.update()
    ```
    *Incrementing if was scored; then updating the variables with the `update()` function.*

    ```python
        def scoringPercentage(self):

            if self.total["runs"] > 0:
                return round((self.total["runs"] / self.total["hits"]) * 100, 2)
    ```
    *Calculating the `runs/hits` percentage if any runs exist; rounding to the second decimal place.*

    ```python
            else:
                return "N/A"
    ```
    *Having a default of `"N/A"` to return in the case of no `runs` recorded.*

    ```python
        def update(self):
            hitNum, runNum = 0, 0
    ```
    *The infamous `update()` function, declaring `hitNum` and `runNum` right off the bat, later to be used for temporary logging.*

    ```python
        for value in self.hits.values():
                hitNum += value
        for value in self.runs.values():
                runNum += value
    ```
    *Running through the value pairs in both variables, logging `hits` and `runs`, being loaded into our temp variables.*

    ```python
        self.total["hits"] = hitNum
        self.total["runs"] = runNum

        self.percentage = self.scoringPercentage()

        return 0
    ```
    *Finally updating our `total` dictionary with the recurred  values. Calculating percentage and rolling the most future calculation in as well, and returning a value of `0` to signfiy a successful run as for the context it being used in.*

## ***Main of the Meat of Code***
 - Now this is where "functional" elements begin to faulter, even though working on both a `win32` and `linux` distrobution, tests on `OSX` are still limited and might break if not carefully ported.
    - Once again, because of this, I do recommed the basic useage of the framework layed out, specifically the structure and concept, rather than actually applications.
    - For this last section once again, and a common theme throughout this whole project, is the lack of good-ness. Don't take this seriously, and with that, less in-dept commentary as well ;)

1. ### Main()

    ```python
    teams = []
    TEAM_SIZE = 9
    first, last = [], []
    ```
    *Declarations for variables to be used later on, sake of readability.*

    ```python
    textfile_directory = os.path.join(os.path.join(os.pardir, os.getcwd()), "txt") if platform != "darwin" else "../txt"
    ```
    *Some python magic allowing good-forsaken things to happen with my directory paths. Essentially evaluates to our wordlist source directory: `../txt`.*

    ```python
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
    ```
    *Randomizing our wordlists and acredditing it to their proportionate dictionary key/value. Unfortunately having to shuffle before splicing down the array, no bully.*

    ```python
    k = 0
    for i in range(0, 2):
        player_list = []
        for j in range(TEAM_SIZE):
            player_list.append(Player(files["first"][k], files["last"][k]))
            k += 1
        teams.append(player_list)
    ```
    *More magic that commenting on at 4AM is most probably not the greatest idea. Not doing it too much credit, but creating the player lists that will eventually get pasted in as the `teams` array. Quite fond of it either way :)*

    ```python
    game = Game(teams)
    game.play()
    ```
    *Creating the new `Game` object and starting it with the predefined `teams` array, as mentioned. Simply letting the code handle it all now.*

    ```python
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
    ```
    *Using the [texttable](https://github.com/foutaise/texttable) to format output data; take a look at it yourself if your curious, just some basic to semi-advanced use of the library.*

    ```python
    table.add_row([game.dump("lastName")[i][j], game.dump("hits['singles']")[i][j], game.dump("hits['doubles']")[i][j], game.dump("hits['triples']")[i][j], game.dump("hits['homes']")[i][j], percentage if isinstance(percentage, str) else f'{round(float(percentage), 2)}%'])
    ```
    *Dissecting one of the lines of code and it's usage with the pre-built function we used earlier `dump()`.*

    *As we can see, we use `game.dump(...)`, inputting our property we want to extract and the two indices, representing the `team` and `player` number.*

    *The using of the `table.add_row(...)`, as well while also setting our proportionate columns and centerings.*

    ```python
    full = table.draw()

    # print(main)
    # print(stats)
    print(full)
    ```
    *Eventually we get to the point that we can print out our table, something in the form:*

    ![TextTable Output](https://i.imgur.com/mD6stWd.png)

*Disclaimer: If you got to the end of this, congrats. This just being a fun little write-up in markdown, I wrote this in a couple hours on a fresh install of VSCode. If you do, magically, want to install this, simply...*

```sh
git clone "https://github.com/WizardDaHacker/game-n-score"
```

*...and then...*

```sh
cd "game-n-score"
poetry install
```

*...and finally to run...*

```sh
poetry run main
```


##### *Developed and manufactured by enslaved elves in wiz's factory...*