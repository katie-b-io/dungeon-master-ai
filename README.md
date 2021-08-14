[![codecov](https://codecov.io/gh/katie-codes-io/dungeon-master-ai/branch/main/graph/badge.svg?token=Q1M90K0HL5)](https://codecov.io/gh/katie-codes-io/dungeon-master-ai)

# dungeon-master-ai
Repo for the Dungeon Master artificial intelligence (DMAI) agent


## Setup

### Docker

The easiest approach is to create a Docker container and run the DMAI from within there. The Dockerfile is included in the top level of this repository and requires a few steps to build an image and run a container:
```
# navigate to the repo
cd dungeon-master-ai

# build the image
docker build --tag dmai --build-arg BUILD_ENV=DEV .

# create the container
docker create --name dmai dmai

# start the container (this will get the Rasa server running - it needs 10-15 seconds before it can begin receiving requests)
docker start dmai

# attach to an interactive shell in the container
docker exec -it dmai bash

# run the DMAI in interactive mode
python3 dungeon-master-ai/dungeon-master.py -i
```

### Manual

The DMAI requires Python 3.8 to run. Make sure `python3.8` is on your PATH by installation or activating a Python 3.8 virtual environment using conda/pyenv/virtualenv.

The dependencies can then be installed with poetry:

`poetry install`

The DMAI requires a Rasa NLU server to be running in API mode and accepting HTTP requests via port 5005: https://rasa.com/docs/rasa/

The DMAI also requires the Fast Downward planner to be installed and on your PATH: https://github.com/aibasel/downward


## Running on the command line
To run the DMAI in interactive mode:

`python ./dungeon-master.py -i`

### Command line arguments

|Argument                |Description                                      |
|------------------------|-------------------------------------------------|
|`-h, --help`            |Show the help message                            |
|`-i, --interactive`     |Run in interactive mode                          |
|`-f, --fighter`         |Play as a fighter                                |
|`-n NAME, --name NAME`  |Set character name (must set character class too)|
|`--skip-intro`          |Skip the intro                                   |
|`--cleanup`             |On exit, remove any files produced during game   |
|`--god-mode`            |Enable god mode, all player rolls return 30      |
|`--no-monsters`         |Disable monsters                                 |

Additional character classes are not fully supported yet:
|Argument                |Description                                      |
|------------------------|-------------------------------------------------|
|`-c, --cleric`          |Play as a cleric                                 |
|`-r, --rogue`           |Play as a rogue                                  |
|`-w, --wizard`          |Play as a wizard                                 |


## Notice of Open Game Content

The DMAI software and *The Tomb of Baradin Stormfury* adventure uses Open Game Content as specified in the *Dungeons & Dragons* System Reference Document version 5.1 (https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf). A list of content used can be found in the Open Game Content markdown file in this repository.
