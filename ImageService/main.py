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
stock -> str: name of images stock to use (pixable \ shutterstock)
keywords -> str | [str]: keywords to search for images
max_images -> int | [int]: max number of images to return
**properties -> dict: holds any other property of stock's API in a dictionary

Returns
-------
list: 
    a list of images url
"""

def main_trigger(stock, keywords, max_images, **properties):
    ret = {}
    if stock == "pixable":
        pixable = stocks.Pixable()
        if type(max_images) is int and type(keywords) is str:
            ans = pixable.get_pictures(keywords, max_images, **properties)
            if type(ans) is int:
                return "error: " + str(ans)
            ret[keywords] = ans

        elif type(max_images) is int and type(keywords) is list:
            for keyword in keywords:
                ans = pixable.get_pictures(keyword, max_images, **properties)
                if type(ans) is int:
                    return "error: " + str(ans)
                ret[keyword] = ans

        elif type(max_images) is list and type(keywords) is list:
            for keyword in keywords:
                ans = pixable.get_pictures(keyword, max_images[keywords.index(keyword)], **properties)
                if type(ans) is int:
                    return "error: " + str(ans)
                ret[keyword] = ans

    elif stock == "shutterstock":
        shutterstock = stocks.Shutterstock()
        if type(max_images) is int and type(keywords) is str:
            ans = shutterstock.get_pictures(keywords, max_images, **properties)
            if type(ans) is int:
                return "error: " + str(ans)
            ret[keywords] = ans

        elif type(max_images) is int and type(keywords) is list:
            for keyword in keywords:
                ans = shutterstock.get_pictures(keyword, max_images, **properties)
                if type(ans) is int:
                    return "error: " + str(ans)
                ret[keyword] = ans

        elif type(max_images) is list and type(keywords) is list:
            for keyword in keywords:
                ans = shutterstock.get_pictures(keyword, max_images[keywords.index(keyword)], **properties)
                if type(ans) is int:
                    return "error: " + str(ans)
                ret[keyword] = ans


    json_obj = json.dumps(ret)
    return json_obj


def main():
   out =main_trigger("pixable", ["banana", "apple"], 5, colors ="green")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("shutterstock", ["dog", "cat"], 5, colors="green")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("pixable", "sun shine", 5, colors="yellow")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("shutterstock", "ground", 5, colors="yellow")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("pixable", ["banana", "apple"], [1, 2], colors="green")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("shutterstock", ["dog", "cat"], [3, 4], colors="green")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("pixable", "sun shine", 5, colors="yellow")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)

   out = main_trigger("shutterstock", "ground", 5, colors="yellow")
   try:
       parsed = json.loads(out)
       print(json.dumps(parsed, indent=4, sort_keys=True))
   except:
       print(out)





if __name__ == '__main__':
    main()