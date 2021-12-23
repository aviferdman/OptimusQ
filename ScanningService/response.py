
class Response:
  Url = ""
  Is_error = False
  Exception = None
  Message = ""
  Keywords = []
  Title = ""
  Description = ""

  def set_url(self,url):
    self.Url=url
    return self

  def get_url(self):
    return self.Url

  def sign_error(self,e, Mes):
    self.Is_error = True
    self.Exception = e
    return self

  def set_messege(self, mes):
    self.Message = mes
    return self

  def set_keywords(self,keywords):
    self.Keywords=keywords
    return self

  def set_title(self,title):
    self.Title=title
    return self

  def set_description(self, des):
    self.Description = des
    return self

  def is_error(self):
    return self.Is_error

  def get_exeption(self):
    return self.Exception

  def get_messege(self):
    return self.Message

  def get_title(self):
    return self.Title

  def get_description(self):
    return self.Description

  def get_keywords(self):
    return self.Keywords