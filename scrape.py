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
      self.scrape_form_info(form, form_information)
      self.write_print_json(form_information)

  def scrape_form_info(self, form, form_information):
    page = 0
    form_number = self.convert_form_num_to_params(form)
    while True:
      start_row = page * 200
      url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow={start_row}&criteria=formNumber&value={form_number}&isDescending=false'
      content = requests.get(url).text
      if content.find('errorText') != -1:
        break
      soup = BeautifulSoup(content, 'lxml')
      if soup.find(text=form.form_number) is None:
        form = "Form Not Found"
        break
      rows = soup.select('.picklistTable tr')
      self.build_form_data(form, rows)
      page +=1
    form_information.append(form)

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

  def build_form_data(self, form, rows):
    rows.pop(0)
    for row in rows:
      if form.form_number == row.select(".LeftCellSpacer")[0].text.strip():
        form.set_title(row.select(".MiddleCellSpacer")[0].text.strip())
        form.year_max(int(row.select(".EndCellSpacer")[0].text.strip()))
        form.year_min(int(row.select(".EndCellSpacer")[0].text.strip()))
    return form




forms = ['Form W-2', 'Form 1099-A']
scrape = Scrape()
scrape.find_forms(forms)
with open('results.json') as json_file:
    data = json.load(json_file)
pprint.pprint(data)
