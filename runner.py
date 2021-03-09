import pprint
import json
from datetime import datetime
from irs_scrape import IrsScrape

class Runner:
  def start(self):
    user_input = input("Are you looking to find form information (1) or download a form by years (2)?\n").strip()
    if user_input == "1":
      self.scrape_form_info()
    elif user_input == "2":
      self.download_form_pdfs()
    else:
      print("I did not understand your selection, please try again!")

  def scrape_form_info(self):
    forms = []
    while True:
      user_input = input("What form would you like to look up information on?\nInput is case sensitive, e.x. 'Form W-2' will have results, 'form w-2' will not.\n").strip()
      forms.append(user_input)
      user_input = input("Would you like to add another form? (y/n)\n").strip()
      if user_input == 'n' or user_input =='no' or user_input =='N' or user_input == "No":
        break
    scrape = IrsScrape()
    scrape.find_forms(forms)
    with open("results.json") as json_file:
        data = json.load(json_file)
    pprint.pprint(data)

  def download_form_pdfs(self):
    this_year = datetime.today().year
    user_input = 0
    form = input("What form are you looking for?\nInput is case sensitive, e.x. 'Form W-2' will have results, 'form w-2' will not.\n").strip()
    while user_input != "1" and user_input != "2":
      user_input = input("Do you need a range of years (1) or specific years (2)?\n").strip()
    parameters = 'invalid'
    while parameters == 'invalid':
      if user_input == "1":
        start_year = int(input("Please input the starting year, e.x. 1960.\n"))
        if start_year >= 1864 and start_year <= (this_year - 1):
          end_year = int(input("Please input the end year, e.x. 2010.\n"))
          if end_year > start_year and end_year <= this_year:
            years = list(range(start_year, end_year))
            parameters = 'valid'
          else:
            print(f"End year must be greater than start year and less than {this_year}.")
        else:
          print(f"Start year needs to be greater than 1863 and not greater than {this_year - 1}")
      if user_input == "2":
        years = []
        while True:
          user_input = int(input(f"For what year would you like to have {form} returned?\n").strip())
          if user_input >= 1864 and user_input <= this_year:
            years.append(user_input)
          else:
            print(f"Invalid year, please input a year between 1864 and {this_year}")
          user_input = input("Would you like to add another year? (y/n)\n").strip()
          if user_input == 'n' or user_input == 'no' or user_input == 'N' or user_input == "No":
            parameters = 'valid'
            break
    scrape = IrsScrape()
    scrape.find_form_by_years(form, years)


start = Runner()
start.start()
