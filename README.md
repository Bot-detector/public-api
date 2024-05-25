# public-api
structure:
- src: contains all program files
- src.api: contains the api
- src.app: contains the database logic
- src.core: contains the core componetns
- src.core.database: contains all the database functionality

# Setup
1. Create fork of primary repo
2. Download a clone of the forked repo `git clone <your github repo path url>`
3. Open a terminal to your cloned repo
4. follow linux or windows sections for further setup
## Windows
creating a python venv to work in and install the project requirements
```sh
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pre-commit install
```
## Linux
Setup overview:
1. install requirements: python, pip, make, docker
2. create venv `python3 -m venv .venv`
3. activate venv `source .venv/bin/activate`
4. run setup `make setup`

detailed guide in sections below

### Install make and pip
#### Debian 
distros such as ubuntu, mint, pop, kali
```sh
sudo apt install make
sudo apt install python3-pip
```

#### Red Hat 
distros such as fedora, centos, rocky
```sh
sudo yum install make
sudo yum install python3-pip
```

#### Arch Linux
```sh
sudo pacman -Syu make
sudo pacman -Syu python3-pip
```

#### MacOS
typically requires xcode command line tools from http://developer.apple.com/ 
or using homebrew from https://brew.sh/ (example below). note the command it installs is `gmake`, ideally just make an alias `make` by adding it to your bash profile
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
Homebrew 4.1.17
brew install make
brew install python3-pip
```

add your alias to your bash profile (loaded on terminal start)
```sh
nano ~/.bash_profile
```

ctrl+x and enter to save once you have added the alias line (example below line to add)
```sh
alias make="gmake"
```

### Python Virtual Enviornment
#### Setup
run the following command to create your venv
```sh
python3 -m venv .venv
```

####  Activate
next command is to activate your virtiual envionrment, you should see to the far left of your prompt showing you what env you are in
```sh
source .venv/bin/activate
```

if you ever need to get out of the virtual enviornment run the `deactivate` command
```sh
deactivate
```

### Make User Guide
use the `make` command with an `action` when developing on linux.  think of `actions` as a list of predefined commands to help simplify common development routines.

#### view avaiable actions
`make help` to see all avaiable actions
```sh
clean-pyc            clean python cache files
clean-test           cleanup pytests leftovers
docker-restart       restart containers
docker-test          restart containers & test
pre-commit-setup     Install pre-commit
test-setup           installs pytest singular package for local testing
requirements         installs all requirements
create-env           create .env file
setup                setup requirements
docs                 opens your browser to the webapps testing docs

```

### Docker
#### Pre-reqs
- docker
- python3
- local clone of repo
- terminal opened to cloned repos root path


#### Setup Docker Environment
With the Makefile we setup our development environment. it is important that you are in your python virtual environment (.venv) when you run this command.
the `make setup` command will 
- create a .env file, 
- install precommit
- install requirements for testing
- install requirements for the project
```sh
make setup
```
You are now ready to develop code but you may want to read further, to know how to run & debug te code

#### Starting / restarting containers
with the Makefile we can easily start & shutdown the containers to a fresh state, under the hood we leverage `docker compose` commands.
```sh
make docker-restart
```

### TDD using pytest
#### Verifying Tests Pass
run `test`
```sh
make docker-test
```

# for admin purposes saving & upgrading
when you added some dependancies update the requirements
```sh
.venv\Scripts\activate
call pip freeze > requirements.txt
```
when you want to upgrade the dependancies
```sh
.venv\Scripts\activate
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '==', '>=' } | Set-Content requirements.txt"
call pip install -r requirements.txt --upgrade
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '>=', '==' } | Set-Content requirements.txt"
```
