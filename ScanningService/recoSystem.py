import re
import urllib.request

import requests
import yake as yake
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

from ScanningService.response import Response


class RecoSystem:


    def scan_landing_page(self, url):
        """
        purpose: scan a landing page url.
        :param url: landing page url
        :return: void
        """

        # opening the url for reading and parsing the html file
        hdr = {'User-Agent': 'Mozilla/5.0'}
        try:
            req = Request(url, headers=hdr)
            page = urlopen(req)
        except Exception as e:
            return None, e
        soup = BeautifulSoup(page)

        return soup, "Success"

    def extract_title_from_landing_page(self, url, htmlParse):
        """
        purpose: extract title from  a landing page.
        :param url: landing page url
        :return: title
        """
        # opening the url for reading
        res = Response()
        res.set_url(url)
        # try:
        #     html = urllib.request.urlopen(url)
        # except Exception as e:
        #     res.sign_error(e,True)
        #     res.set_messege("cant open the url")
        #     return res

        # parsing the html file
        title = htmlParse.find('title')
        if title is None:
           res.sign_error(None,True)
           res.set_messege("Cannot extract title")
           return res
        return res.set_title(title.text)

    def extract_description_from_landing_page(self, url, htmlParse):
        res = Response()
        res.set_url(url)
        head = htmlParse.find("head")
        description = ""
        for t in head:
            if str(t).__contains__("name=\"description\"") and str(t).__contains__("meta"):
                if str(t).__contains__("content"):
                    description = t.__getitem__("content")
                    break
        if description == "":
            res.sign_error(None, True)
            res.set_messege("Cannot extract description")
            return res
        else:
            return res.set_description(description)

    def extract_keywords_from_landing_page(self, url, htmlParse):
        """
        purpose: extract keywords from  a landing page.
        :param url: landing page url
        :return: list of keywords
        """
        response = Response()
        response.set_url(url)

        title = htmlParse.find("title")
        if title is None:
            response.sign_error(None, True)
            response.set_messege("Cannot extract keywords")
            return response
            # return ["Exception: Cannot Access url"]

        head = htmlParse.find("head")
        str_of_keywords = ""
        for t in head:
            if str(t).__contains__("name=\"keywords\"") and str(t).__contains__("meta"):
                if str(t).__contains__("content"):
                    str_of_keywords = t.__getitem__("content")
                    break

        if str_of_keywords != "":
            res = str_of_keywords.split(',')
            # if len(res) < 5:
            #     return response.set_keywords(res)
            return response.set_keywords(res)

        # checks if str in part of a title or a header

        def check_if_in_title(title, str):
            if str in title:
                return True
            return False

        def check_if_in_header(htmlParse, h_i, str):
            headers = htmlParse.find_all(h_i)
            if (type(headers) == type(None)) or (len(headers) == 0):
                return False
            for t in headers:
                if str.lower() in t.text.lower():
                    return True
            return False

        # dictionary for score
        score_dict = {'title': 0.07, 'h1': 0.06, 'h2': 0.05, 'h3': 0.04,
                      'h4': 0.03, 'h5': 0.02, 'h6': 0.01}
        paragraphs = ""
        paragraph_tags = htmlParse.find_all('p')
        for p in paragraph_tags:
            paragraphs += str(p.text).lower()

        if len(paragraphs) <= 5 or re.search('[a-zA-Z]', paragraphs) is None:
            paragraphs = title.text
            print("hay!")
            # return response.set_keywords([title.text])

        language = "en"
        max_ngram_size = 2
        deduplication_threshold = 0.9
        numOfKeywords = 20
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                    top=numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(paragraphs)
        res_list = []
        for kw in keywords:
            new_score = kw[1]
            if check_if_in_title(title.text.lower(), str(kw[0]).lower()):
                new_score = kw[1] * (1 - score_dict['title'])
            for i in range(1, 7):
                if check_if_in_header(htmlParse, 'h' + str(i), str(kw[0]).lower()):
                    new_score = kw[1] * (1 - score_dict['h' + str(i)])
            new_tuple = (kw[0], new_score)
            res_list.append(new_tuple)

        def key_func(tuple):
            return tuple[1]

        res_list.sort(key=key_func)
        res = []
        for w in res_list:
            res.append(w[0])

        return response.set_keywords(res)

    def scrap_page(self, url):
        if url is None or url == "":
            return {"title": "",
                    "description": "",
                    "keywords": []}
        htmlParse, e = self.scan_landing_page(url)
        if htmlParse is None:
            return {"title": "cant open the url",
                    "description": "cant open the url",
                    "keywords": []}
        response = self.extract_title_from_landing_page(url, htmlParse)
        if response.is_error():
            title = response.get_messege()
        else:
            title = response.get_title()
        response = self.extract_description_from_landing_page(url, htmlParse)
        if response.is_error():
            description = response.get_messege()
        else:
            description = response.get_description()
        response = self.extract_keywords_from_landing_page(url, htmlParse)
        if response.is_error():
            keywords = []
        else:
            keywords = response.get_keywords()

        dict = {"title": title,
                "description": description,
                "keywords": keywords}

        return dict
