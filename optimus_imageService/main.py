import string
import stocks

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
keywords -> str: keywords to search for images
max_images -> int: max number of images to return
**properties -> dict: holds any other property of stock's API in a dictionary

Returns
-------
list: 
    a list of images url
"""

def get_images(stock, keywords, max_images, **properties):
    ret = []
    if stock == "pixable":
        pixable = stocks.Pixable()
        ret = pixable.get_pictures(keywords, max_images, **properties)

    elif stock == "shutterstock":
        shutterstock = stocks.Shutterstock()
        ret = shutterstock.get_pictures(keywords, max_images, **properties)

    return ret

def main():
   print(get_images("pixable", "banana", 5, colors = "green"))


if __name__ == '__main__':
    main()