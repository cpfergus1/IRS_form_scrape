from bs4 import BeautifulSoup
import math
import requests
import json
import os.path
from form import Form


class IrsScrape:

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
      url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow={start_row}&criteria=formNumber&value={form_number}&isDescending=false"
      content = requests.get(url).text
      if content.find("errorText") != -1:
        break
      soup = BeautifulSoup(content, "lxml")
      if page == 0 and soup.find(text=form.form_number) is None:
        form = "Form Not Found"
        break
      rows = soup.select(".picklistTable tr")
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
    with open("results.json", "w") as outfile:
      json.dump(data, outfile)
    print('Results written to results.json')

  def build_form_data(self, form, rows):
    rows.pop(0)
    for row in rows:
      if form.form_number == row.select(".LeftCellSpacer")[0].text.strip():
        form.set_title(row.select(".MiddleCellSpacer")[0].text.strip())
        form.year_max(int(row.select(".EndCellSpacer")[0].text.strip()))
        form.year_min(int(row.select(".EndCellSpacer")[0].text.strip()))
    return form

  def find_form_by_years(self, form_number, years):
    for year in years:
      pdf_link = self.search_form(form_number, year)
      if pdf_link is not None:
        response = requests.get(pdf_link)
        self.create_pdf(response, form_number, year)
        print(f"Created {form_number} for {year}!")


  def search_form(self, form_number, year):
    page = 0
    while True:
      start_row = page * 200
      url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow={start_row}&criteria=currentYearRevDateString&value={year}&isDescending=false"
      content = requests.get(url).text
      soup = BeautifulSoup(content, "lxml")
      if content.find("errorText") != -1:
        print(f"Cannot find {form_number} for {year}")
        break
      if soup.find("a", text=form_number) is not None:
        return soup.find("a", href=True, text=form_number)['href']
      page += 1

  def create_pdf(self, response, form_number, year):
    file_path = "forms/" + form_number + " - " + str(year) + ".pdf"
    open(file_path, 'wb').write(response.content)
