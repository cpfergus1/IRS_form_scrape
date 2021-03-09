# IRS_form_scrape
# README

## Table of Contents:

- [Overview](#overview)
- [Techstack](#techstack)
- [Local Setup](#setup)
- [Running Locally](#running)

## Overview of Application
This is a python web scraping application designed to pull information on your desired IRS forms or download available form based on year it was updated! The application is CLI promted and will take your inputs and return either the form information with earliest and latest years the form has been updated or it will download a form for a range, or specific years. User inputs are stored temporarily in the runner file as arrays and sent to the irs_scrape.py for processing. 

Output from the program will come in three different ways:

- JSON Text display in CLI
```
Results written to results.json
[{'form_number': 'Form W-2',
  'form_title': 'Wage and Tax Statement (Info Copy Only)',
  'max_year': 2021,
  'min_year': 1954},
 {'form_number': 'Form W-2 P',
  'form_title': 'Statement For Recipients of Annuities, Pensions, Retired Pay, '
                'or IRA Payments',
  'max_year': 1990,
  'min_year': 1971},
 {'form_number': 'Form 1099-A',
  'form_title': 'Acquisition or Abandonment of Secured Property (Info Copy '
                'Only)',
  'max_year': 2021,
  'min_year': 1977}]
```
- Results.json file in application root directory will be created
- Tax form downloads will be saved to the `application root dir/forms/{form-name - form-year}.pdf` e.x. `IRS_form_scrape/forms/Form W-2 - 2001.pdf`

Potential future functionality will include:
 - Proccessing a base file instead of CLI inputs if desired.
 - Updating runner file logic for error handling
 - Potential GUI
 - Implment case insensitivity on input
 - Threading/Job Queues for parallel processing

## Techstack/Libraries

- Python 3.9.2
- BeautifulSoup
- lxml
- requests
- pprint


## Setup
- clone this repo locally.
- install python 3.9.2 if your version of python is not already compatible.
- install the latest dependent libraries:
```
pip3 install requests
pip3 install beautifulsoup4
pip3 install pprint
pip3 install lxml
```
## Running Locally

navigate to your cloned repo folder location in CLI
- in CLI run: `python3 runner.rb`
- follow CLI prompts to retrieve desired data
- file generated by this program can be found in your cloned repo path within the forms folder.

## Notes to potential future employer

This was my very first full python application that I am excited to share with you! I beleive the most difficult part of this challenge was navigating my way through BeautifulSoup and getting to the elements I needed. Additionally, because this was my first python app, there was a little bit of a learning curve with the language. I felt the similarities to Ruby helped me develop this app in a decent amount of time. Thanks for letting me participate!

