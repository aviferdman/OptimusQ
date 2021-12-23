import requests
import json


ImageServicePropertiesURL = "https://optimusqbgu.azurewebsites.net/api/ManagementService"

def send_post_request(url, body):
    respons = requests.post(url, json=body)
    jsonResponse=respons.content
    return json.loads(jsonResponse)

def main_trigger(url):
    dictionary = send_post_request(ImageServicePropertiesURL,{"landingPage":url, "stock":"pixable","imageServiceProperties":{}})
    return dictionary

 # response = requests.get(url)
    # try:
    #     request_body = req.get_json()
    # except:
    #     return "Empty Body"
    # landingPage =  request_body["landingPage"]
 