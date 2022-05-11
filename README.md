# Project Setup

[![Production Workflow 1](https://github.com/cle4njit/project4/actions/workflows/prod.yml/badge.svg)](https://github.com/cle4njit/project4/actions/workflows/prod.yml)

* [Production Deployment](https://cle4-prod-final.herokuapp.com/)


[![Development Workflow 3.8](https://github.com/cle4njit/project4/actions/workflows/dev.yml/badge.svg)](https://github.com/cle4njit/project4/actions/workflows/dev.yml)

* [Developmental Deployment](https://cle4-dev-final1.herokuapp.com/)


## Setting up CI/CD

The result of this will be that when you create a pull request to merge a branch to master, it will deploy to your
heroku development app/dyno and when you merge or push to master on github, it will deploy the app to the production heroku
app/dyno.

## Running Locally

1. To Build with docker compose:
   docker compose up --build
2. To run tests, Lint, and Coverage report use this command: pytest --pylint --cov

.pylintrc is the config for pylint, .coveragerc is the config for coverage and setup.py is a config file for pytest
