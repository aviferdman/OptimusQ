import azure.functions
import string
try:
    from . import stocks
except:
    import stocks
import json

maxValidKeyword = 5

def read_data():
    path = "data.txt"
    lines = []
    with open(path) as f:
        lines = f.readlines()
    return lines

def getKeywords(data):
    ret = []
    lines = read_data()
    for line in lines:
        ret.extend(line.split(","))
    ret = eliminateWhiteChars(ret)
    return ret

def eliminateWhiteChars(li):
    new_li = []
    for element in li:
        new_elem = element.translate({ord(i): None for i in string.whitespace})
        new_li.append(new_elem)
    return new_li

"""
Retrieve list of images according to search's keywords

Parameters
----------
Http request including json with the following fields:
stock -> str: name of images stock to use from {pixable,  shutterstock}
keywords -> [str]: keywords to search for images
max_images -> [int]: max number of images to return
properties -> dict: holds any other property of stock's API in a dictionary

Returns
-------
list: 
    a list of images url
    
stock, keywords, max_images, **properties    
"""
def main_trigger(req: azure.functions.HttpRequest):
    ret = None
    try:
        js = req.get_json()
    except:
        return {"images": {}}
    stock = js["stock"]
    stock = stock.translate({ord(i): None for i in string.whitespace})
    keywords = js["keywords"]
    max_images = js["maxImages"]
    properties = js["properties"]
    valid = validInput(stock, keywords, max_images, properties)
    if not valid:
        return {"images": {}}

    if stock == "pixable":
        ret = getImagePixable(keywords, max_images, properties)
    elif stock == "shutterstock":
        ret = getImageShutterStock(keywords, max_images, properties)


    return {"images": ret}

def main_trigger_json(js):
    ret = None
    stock = js["stock"]
    stock = stock.translate({ord(i): None for i in string.whitespace})
    keywords = js["keywords"]
    max_images = js["maxImages"]
    properties = js["properties"]
    valid = validInput(stock, keywords, max_images, properties)
    if not valid:
        return {"images": {}}

    if stock == "pixable":
        ret = getImagePixable(keywords, max_images, properties)
    elif stock == "shutterstock":
        ret = getImageShutterStock(keywords, max_images, properties)

    return {"images": ret}

def validInput(stock, keywords, max_images, properties):
    if stock != "pixable" and stock != "shutterstock":
        return False

    if type(keywords) is not list or type(max_images) is not list or type(properties) is not dict:
        return False

    if len(keywords) != len(max_images):
        return False

    if not(all(isinstance(item, str) for item in keywords) and all(isinstance(item, int) for item in max_images)):
        return False

    return True

def getImagePixable(keywords, max_images, properties):
    global maxValidKeyword
    ret = {}
    pixable = stocks.Pixable()
    for keyword in keywords:
        if len(ret.keys()) >= maxValidKeyword:
            break
        try:
            ans = pixable.get_pictures(keyword, max_images[keywords.index(keyword)], properties)
            if type(ans) is int:
                raise Exception("Error: " + str(ans))
            if ans:
                ret[keyword] = ans

        except:
            # need to record error in logger
            continue

    return ret

def getImageShutterStock(keywords, max_images, properties):
    global maxValidKeyword
    ret = {}
    shutterStock = stocks.Shutterstock()
    for keyword in keywords:
        if len(ret.keys()) >= maxValidKeyword:
            break
        try:
            ans = shutterStock.get_pictures(keyword, max_images[keywords.index(keyword)], properties)
            if type(ans) is int:
                raise Exception("Error: " + str(ans))
            if ans:
                ret[keyword] = ans

        except:
            # need to record error in logger
            continue

    return ret

def test():
    dict_1 = {
        "stock": "shutterstock",
        "keywords": ["banana", "apple", "egg", "monkey"],
        "maxImages": [5, 4, 3, 2],
        "properties": {}
    }

    dict_2 = {
        "stock": "shutterstock",
        "keywords": ["apple"],
        "maxImages": [3, 1],
        "properties": {}
    }

    dict_3 = {
        "stock": "shutterstock",
        "keywords": ["banana", "apple"],
        "maxImages": [3],
        "properties": {}
    }

    dict_4 = {
        "stock": "shutterstock",
        "keywords": ["banana", "apple"],
        "maxImages": [3, 1],
        "properties": "wowow"
    }

    dict_5 = {
        "stock": "pixable",
        "keywords": [],
        "maxImages": [],
        "properties": {}
    }

    dict_6 = {
        "stock": "pixable",
        "keywords": ["banana"],
        "maxImages": [5],
        "properties": {}
    }

    dict_7 = {
        "stock": "pixable",
        "keywords": ["banana", "apple"],
        "maxImages": [3],
        "properties": {}
    }

    dict_8 = {
        "stock": "pixable",
        "keywords": ["apple"],
        "maxImages": [3, 1],
        "properties": "nana"
    }

    dict_9 = {
        "stock": "pixable",
        "keywords": ["apple"],
        "maxImages": [3, "banana"],
        "properties": {}
    }

    dict_10 = {
        "stock": "pixable",
        "keywords": ["apple", 3],
        "maxImages": [3, 1],
        "properties": {}
    }

    dict_11 = {
        "stock": "shoko",
        "keywords": ["sky"],
        "maxImages": [7],
        "properties": {}
    }

    print("1:")
    out = main_trigger_json(dict_1)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("2:")
    out = main_trigger_json(dict_2)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("3:")
    out = main_trigger_json(dict_3)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("4:")
    out = main_trigger_json(dict_4)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("5:")
    out = main_trigger_json(dict_5)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("6:")
    out = main_trigger_json(dict_6)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("7:")
    out = main_trigger_json(dict_7)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("8:")
    out = main_trigger_json(dict_8)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("9:")
    out = main_trigger_json(dict_9)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("10:")
    out = main_trigger_json(dict_10)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

    print("11:")
    out = main_trigger_json(dict_11)
    images = out["images"]
    images = json.dumps(images, indent=4)
    print(images)

def main():
    test()


if __name__ == '__main__':
    main()