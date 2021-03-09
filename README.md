# IRS_form_scrape
# README

## Table of Contents:

- [Overview](#overview)
- [Techstack](#techstack)
- [Local Setup](#setup)
- [Running Locally](#running)

## Overview of Application
This is my first python web scraping application designed to pull information on your desired IRS forms or download available form based on year it was updated!

Future functionality will include:
 - Proccessing a base file instead of CLI inputs if desired.
 - Updating runner file logic for error handling
 - Potential GUI

## Techstack/Libraries

- Python 3.9.2
- BeautifulSoup
- lxml
- requests
- pprint


## Setup
- clone this repo locally.
- install python 3.9.2 if your version of python is not already compatible.
- install the latest libraries:
```
pip3 install requests
pip3 install beautifulsoup4
pip3 install pprint
pip3 install lxml
```
## Running Locally

navigate to your cloned repo
- in CLI run: `python3 runner.rb`
- follow CLI prompts to retrieve desired data
- file generated by this program can be found in your cloned repo path within the forms folder.
