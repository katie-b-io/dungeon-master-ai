[![codecov](https://codecov.io/gh/katie-codes-io/dungeon-master-ai/branch/main/graph/badge.svg?token=Q1M90K0HL5)](https://codecov.io/gh/katie-codes-io/dungeon-master-ai)

# dungeon-master-ai
Repo for the Dungeon Master artificial intelligence (DMAI) agent

### Setup
The DMAI requires Python 3.8 to run. Make sure `python3.8` is on your PATH by installation or activating a Python 3.8 virtual environment using conda/pyenv/virtualenv.

The dependencies can then be installed with poetry:

`poetry install`

### Running on the command line
To run the DMAI in interactive mode:

`python ./dungeon-master.py -i`

### Command line arguments

|Argument                |Description                                      |
|------------------------|-------------------------------------------------|
|`-h, --help`            |Show the help message                            |
|`-i, --interactive`     |Run in interactive mode                          |
|`-c, --cleric`          |Play as a cleric                                 |
|`-f, --fighter`         |Play as a fighter                                |
|`-r, --rogue`           |Play as a rogue                                  |
|`-w, --wizard`          |Play as a wizard                                 |
|`-n NAME, --name NAME`  |Set character name (must set character class too)|
|`--skip-intro`          |Skip the intro                                   |
|`--cleanup`             |On exit, remove any files produced during game   |
|`--god-mode`            |Enable god mode, all player rolls return 30      |
|`--no-monsters`         |Disable monsters                                 |