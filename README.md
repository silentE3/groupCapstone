# Grooper
[![codecov](https://codecov.io/gh/zredinger/team-58/branch/main/graph/badge.svg?token=UEEKNFR2WG)](https://codecov.io/gh/zredinger/team-58)
## Setup
Run these commands in the root context of the repository

1. Install python 3.10.* [Download here](https://www.python.org/downloads/)
2. Install pipenv
``` 
pip install pipenv
```
3. Install pipenv to manage dependencies and virtual envs
```
pipenv install
```
4. Start the virtual environment
 ```
 pipenv shell
 ```
5. Run the code
```
python file.py
```

## CI Configuration

A Github action has been configured in this repository for managing the Continuous Integration flow after opening a PR. The action currently runs a couple of things against the source code and requires that they pass before merging pull requests:
- unit tests - pytest is used to run unit tests
- linter - pylint is our linter of choice



