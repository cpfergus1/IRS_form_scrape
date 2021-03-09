class Form:

  def __init__(self, number):
    self.form_number = number
    self.form_title = ''
    self.min_year = 2021
    self.max_year = 0

  def year_max(self, year):
    if ( year > self.max_year ):
      self.max_year = year

  def year_min(self, year):
    if ( year < self.min_year ):
      self.min_year = year

  def set_title(self, title):
    if ( self.form_title != title ):
      self.form_title = title
