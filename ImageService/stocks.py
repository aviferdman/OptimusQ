import requests
import string
import json

class Pixable:
  def __init__(self):
      self.api_key = "24751437-3093e242edb642b02ce14bc2a"
      self.api = "https://pixabay.com/api/"

  def get_pictures(self, keywords, max_images, properties):
      images = []
      req = self.api + "?key = " + self.api_key + "&q = " + keywords
      for key in properties:
          req = req + "&" + key + "=" + properties[key]
      new_req = req.translate({ord(i): None for i in string.whitespace})
      response = requests.get(new_req)
      if response.ok:
          js = response.json()
          hits = js["hits"]
          for hit in hits:
            if len(images) == max_images:
                break
            images.append(hit["webformatURL"])
          return images
      else:
          return response.status_code


class Shutterstock:
  def __init__(self):
      self.key = "DJM1XdGRsM5A9o336muQ0fVpVtNHma5D"
      self.secret = "G1k25v5sbDJ52iEc"
      self.api = "https://api.shutterstock.com/v2/images/search"

  def get_pictures(self, keywords, max_images, properties):
     images = []
     req = self.api + "?query = " + keywords
     for key in properties:
         req = req + "&" + key + "=" + properties[key]
     new_req = req.translate({ord(i): None for i in string.whitespace})
     response = requests.get(new_req, auth=(self.key, self.secret))
     if response.ok:
         js = response.json()
         data = js["data"]
         for image in data:
             if len(images) == max_images:
                 break
             images.append(image["assets"]["preview"]["url"])
         return images
     else:
        return response.status_code


class Istock:
  def __init__(self):
      pass


