Url=""
is_error=False
Exception=None
Messege=""
Kywords=[]
Title=""

class Response:
  def set_url(url):
    Url=url

  def sign_error(e, Mes):
    is_error = True
    Exception = e
    return None

  def add_messegr(mes):
    Messege = mes
    return None

  def add_keywords(keywords):
    Keywords=keywords
    return None

  def add_title(title):
    Title=title
    return None

  def is_error():
    return is_error

  def get_exeption():
    return Exception

  def get_messege():
    return Messege

  def get_title():
    return Title




