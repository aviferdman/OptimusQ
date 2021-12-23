import azure.functions
import string
import json
import requests

ScannerURL = "https://scanneroq.azurewebsites.net/api/scannertrigger"
ImageServiceURL = "https://optimusqbgu.azurewebsites.net/api/imageservice"
DataBaseServiceURL = "https://optimusqbgu.azurewebsites.net/api/databaseservice"
DebugImageServiceURL = "http://localhost:7071/api/ImageService"
DebugDataBaseServiceURL = "http://localhost:7071/api/DataBaseService"
MaxImagesPerKeyword = 1

def send_post_request(url, body):
    response = requests.post(url, json = body)
    jsonResponse = response.content
    return json.loads(jsonResponse)

def main_trigger(req: azure.functions.HttpRequest):
    try:
        request_body = req.get_json()
    except:
        return "Empty Body"
    landingPage = request_body["landingPage"]
    stock = request_body["stock"]
    image_service_properties = {}
    if "imageServiceProperties" in request_body:
        image_service_properties = request_body["imageServiceProperties"]
    dictionary = send_post_request(ScannerURL, {"landingPage": landingPage})
    keywords = dictionary["keywords"]
    maxImages = [MaxImagesPerKeyword for i in keywords]
    images_dict = send_post_request(ImageServiceURL, { "stock": stock, "keywords": keywords, "maxImages": maxImages, "properties": image_service_properties })
    dictionary.update(images_dict)
    db_dict = dictionary.copy()
    db_dict.update({"landingPage": landingPage})
    send_post_request(DataBaseServiceURL, db_dict)

    return dictionary