import azure.functions
import string
import stocks
import json

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
        return "Empty Body"
    stock = js["stock"]
    stock = stock.translate({ord(i): None for i in string.whitespace})
    keywords = js["keywords"]
    max_images = js["max_images"]
    properties = js["properties"]
    valid = validInput(stock, keywords, max_images, properties)
    if not valid[0]:
        return "Error: " + valid[1]

    if stock == "pixable":
        ret = getImagePixable(keywords, max_images, properties)
    elif stock == "shutterstock":
        ret = getImageShutterStock(keywords, max_images, properties)

    if type(ret) is not dict:
        return ret

    json_obj = json.dumps(ret)
    return json_obj

def main_trigger_json(js):
    ret = None
    # js = req.get_json()
    js = json.loads(js)
    if not js:
        return "Empty Json"
    stock = js["stock"]
    stock = stock.translate({ord(i): None for i in string.whitespace})
    keywords = js["keywords"]
    max_images = js["max_images"]
    properties = js["properties"]
    valid = validInput(stock, keywords, max_images, properties)
    if not valid[0]:
        return "Error: " + valid[1]

    if stock == "pixable":
        ret = getImagePixable(keywords, max_images, properties)
    elif stock == "shutterstock":
        ret = getImageShutterStock(keywords, max_images, properties)

    if type(ret) is not dict:
        return ret

    json_obj = json.dumps(ret)
    return json_obj

def validInput(stock, keywords, max_images, properties):
    if stock != "pixable" and stock != "shutterstock":
        return False, "stock name should be from: {pixable, shutterstock}"

    if type(keywords) is not list or type(max_images) is not list or type(properties) is not dict:
        return False, "type error"

    if len(keywords) != len(max_images):
        return False, "list length error"

    if not(all(isinstance(item, str) for item in keywords) and all(isinstance(item, int) for item in max_images)):
        return False, "list type error"

    return True,

# def main_trigger(stock, keywords, max_images, **properties):
#     error = False
#     ret = {}
#     if stock == "pixable":
#         if type(max_images) is int and type(keywords) is str:
#             error = getImagePixable(keywords, max_images, ret, **properties)
#
#         elif type(max_images) is int and type(keywords) is list:
#             for keyword in keywords:
#                 error = getImagePixable(keyword, max_images, ret, **properties)
#
#         elif type(max_images) is list and type(keywords) is list:
#             for keyword in keywords:
#                 error = getImagePixable(keyword, max_images[keywords.index(keyword)], ret, **properties)
#
#     elif stock == "shutterstock":
#         if type(max_images) is int and type(keywords) is str:
#             error = getImageShutterStock(keywords, max_images, ret, **properties)
#
#         elif type(max_images) is int and type(keywords) is list:
#             for keyword in keywords:
#                 error = getImageShutterStock(keyword, max_images, ret, **properties)
#
#         elif type(max_images) is list and type(keywords) is list:
#             for keyword in keywords:
#                 error = getImageShutterStock(keyword, max_images[keywords.index(keyword)], ret, **properties)
#
#     if error:
#         return "Error: " + str(error)
#
#     json_obj = json.dumps(ret)
#     return json_obj

# def getImagePixable(keywords, max_images, ret, **properties):
#     try:
#         pixable = stocks.Pixable()
#         ans = pixable.get_pictures(keywords, max_images, **properties)
#         if type(ans) is int:
#             raise Exception("Error: " + str(ans))
#
#     except:
#         error = ans
#         return error
#
#     ret[keywords] = ans
#
# def getImageShutterStock(keywords, max_images, ret, **properties):
#     try:
#         shutterstock = stocks.Shutterstock()
#         ans = shutterstock.get_pictures(keywords, max_images, **properties)
#         if type(ans) is int:
#             raise Exception("Error: " + str(ans))
#     except:
#         error = ans
#         return error
#
#     ret[keywords] = ans

def getImagePixable(keywords, max_images, properties):
    ret = {}
    try:
        pixable = stocks.Pixable()
        for keyword in keywords:
            ans = pixable.get_pictures(keyword, max_images[keywords.index(keyword)], properties)
            if type(ans) is int:
                raise Exception("Error: " + str(ans))
            ret[keyword] = ans

    except:
        error = ans
        return "error: " + str(error)

    return ret

def getImageShutterStock(keywords, max_images, properties):
    ret = {}
    try:
        shutterstock = stocks.Shutterstock()
        for keyword in keywords:
            ans = shutterstock.get_pictures(keyword, max_images[keywords.index(keyword)], properties)
            if type(ans) is int:
                raise Exception("Error: " + str(ans))
            ret[keyword] = ans

    except:
        error = ans
        return "error: " + str(error)

    return ret

def test():
    dict_1 = {
        "stock": "shutterstock",
        "keywords": ["banana", "apple"],
        "max_images": [3, 1],
        "properties": {}
    }

    dict_2 = {
        "stock": "shutterstock",
        "keywords": ["apple"],
        "max_images": [3, 1],
        "properties": {}
    }

    dict_3 = {
        "stock": "shutterstock",
        "keywords": ["banana", "apple"],
        "max_images": [3],
        "properties": {}
    }

    dict_4 = {
        "stock": "shutterstock",
        "keywords": ["banana", "apple"],
        "max_images": [3, 1],
        "properties": "wowow"
    }

    dict_5 = {
        "stock": "pixable",
        "keywords": [],
        "max_images": [],
        "properties": {}
    }

    dict_6 = {
        "stock": "pixable",
        "keywords": ["sky"],
        "max_images": [7],
        "properties": {}
    }

    dict_7 = {
        "stock": "pixable",
        "keywords": ["banana", "apple"],
        "max_images": [3],
        "properties": {}
    }

    dict_8 = {
        "stock": "pixable",
        "keywords": ["apple"],
        "max_images": [3, 1],
        "properties": "nana"
    }

    dict_9 = {
        "stock": "pixable",
        "keywords": ["apple"],
        "max_images": [3, "banana"],
        "properties": {}
    }

    dict_10 = {
        "stock": "pixable",
        "keywords": ["apple", 3],
        "max_images": [3, 1],
        "properties": {}
    }

    dict_11 = {
        "stock": "shoko",
        "keywords": ["sky"],
        "max_images": [7],
        "properties": {}
    }

    js_1 = json.dumps(dict_1, indent=4)
    js_2 = json.dumps(dict_2, indent=4)
    js_3 = json.dumps(dict_3, indent=4)
    js_4 = json.dumps(dict_4, indent=4)
    js_5 = json.dumps(dict_5, indent=4)
    js_6 = json.dumps(dict_6, indent=4)
    js_7 = json.dumps(dict_7, indent=4)
    js_8 = json.dumps(dict_8, indent=4)
    js_9 = json.dumps(dict_9, indent=4)
    js_10 = json.dumps(dict_10, indent=4)
    js_11 = json.dumps(dict_11, indent=4)

    print("1:")
    out = main_trigger_json(js_1)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("2:")
    out = main_trigger_json(js_2)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("3:")
    out = main_trigger_json(js_3)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("4:")
    out = main_trigger_json(js_4)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("5:")
    out = main_trigger_json(js_5)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("6:")
    out = main_trigger_json(js_6)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("7:")
    out = main_trigger_json(js_7)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("8:")
    out = main_trigger_json(js_8)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("9:")
    out = main_trigger_json(js_9)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("10:")
    out = main_trigger_json(js_10)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

    print("11:")
    out = main_trigger_json(js_11)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    except:
        print(out)

def main():
    test()


if __name__ == '__main__':
    main()