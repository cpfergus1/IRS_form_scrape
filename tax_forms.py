from bs4 import BeautifulSoup
import math
import requests
import json
import pprint
from form import Form

class Scrape:

  def find_forms(self, form_numbers):
    form_information = []
    for form_number in form_numbers:
      form = Form(form_number)
      num_pages = self.find_num_pages(form)
      self.get_data(form, num_pages, form_information)
      self.write_print_json(form_information)

  def find_num_pages(self, form):
    form_number = self.convert_form_num_to_params(form)
    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={form_number}&isDescending=false'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    if soup.find(text=form.form_number) is None:
      return "Form Not Found"
    results = self.extract_number_results(soup)
    return math.ceil(results/200)

  def extract_number_results(self, soup):
    results_text = soup.select('.ShowByColumn')[0].text
    results_array = [int(i) for i in results_text.split() if i.isdigit()]
    return results_array[-1]

  def scrape_form_info(self, form, i):
    start_row = i * 200
    form_number = self.convert_form_num_to_params(form)
    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow={start_row}&criteria=formNumber&value={form_number}&isDescending=false'
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    rows = soup.select('.picklistTable tr')
    rows.pop(0)
    for row in rows:
      if form.form_number == row.select(".LeftCellSpacer")[0].text.strip():
        form.set_title(row.select(".MiddleCellSpacer")[0].text.strip())
        form.year_max(int(row.select(".EndCellSpacer")[0].text.strip()))
        form.year_min(int(row.select(".EndCellSpacer")[0].text.strip()))
    return form

  def convert_form_num_to_params(self, form):
    return form.form_number.replace(" ", "+")

  def write_print_json(self, forms):
    data = []
    for form in forms:
      if isinstance(form, str):
        json_form = {
          "error": form
        }
      else:
        json_form = {
          "form_number": form.form_number,
          "form_title": form.form_title,
          "min_year": form.min_year,
          "max_year": form.max_year
        }
      data.append(json_form)
    with open('results.json', 'w') as outfile:
      json.dump(data, outfile)

  def get_data(self, form, num_pages, form_information):
    if num_pages == "Form Not Found":
      form_information.append(f"{form.form_number} was not found")
    elif num_pages > 1:
      for i in range(0, num_pages-1):
        form_information.append(self.scrape_form_info(form, i))
    else:
      form_information.append(self.scrape_form_info(form, 0))
    return form_information

  #def find_form_by_dates(self, form, dates)


forms = ['Form W-2', 'Form 1099-A']
scrape = Scrape()
scrape.find_forms(forms)
with open('results.json') as json_file:
    data = json.load(json_file)
pprint.pprint(data)
