import re
import yake as yake
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

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
        purpose: extract title from a landing page.
        :param url: landing page url
        :param htmlParse: text of html page
        :return: title
        """
        # opening the url for reading
        res = Response()
        res.set_url(url)

        # parsing the html file
        # find the title tag in the html file. If there is no title tag, error is sending in the response
        title = htmlParse.find('title')
        if title is None:
            res.sign_error(None, True)
            res.set_messege("Can't extract title")
            return res
        return res.set_title(title.text)

    def extract_description_from_landing_page(self, url, htmlParse):
        """
        purpose: extract description from a landing page.
        :param url: landing page url
        :param htmlParse: text of html page
        :return: description
        """

        # searching 'description' tag from 'head' tag
        res = Response()
        res.set_url(url)
        head = htmlParse.find("head")
        description = ""
        for t in head:
            if str(t).__contains__("name=\"description\"") and str(t).__contains__("meta"):
                if str(t).__contains__("content"):
                    description = t.__getitem__("content")
                    break

        # if description not found, return an appropriate message
        if description == "":
            res.sign_error(None, True)
            res.set_messege("can't extract description")
            return res
        else:
            return res.set_description(description)

    def extract_keywords_from_landing_page(self, url, htmlParse):
        """
        purpose: extract keywords from  a landing page.
        :param url: landing page url
        :param htmlParse: text of html page
        :return: if 'keywords' tag found in the html page, return it. else, return list of keywords based on our algorithm
        """
        response = Response()
        response.set_url(url)

        # search for 'title' tag in order to use it in the algorithm, to extract keywords.
        title = htmlParse.find("title")
        if title is None:
            response.sign_error(None, True)
            response.set_messege("can't extract keywords")
            return response

        # some html files contains keywords, which are relevant for us
        head = htmlParse.find("head")
        str_of_keywords = ""
        for t in head:
            if str(t).__contains__("name=\"keywords\"") and str(t).__contains__("meta"):
                if str(t).__contains__("content"):
                    str_of_keywords = t.__getitem__("content")
                    break

        if str_of_keywords != "":
            res = str_of_keywords.split(',')
            return response.set_keywords(res)

        # ***if we didn't find 'keywords' tag , continue to our algorithm***
        # The main idea is to calculate of the score for each keyword,
        # that will be determined according to the frequency of the word appearing on the landing page
        # and will also be given extra points if the word appears in the title or one of the headers.

        # find the title and headers on the page,
        # and each word that appears on the page is given a higher score, if it appears in at least one of them.
        def check_if_in_title(titleToCheck, string):
            if string in titleToCheck:
                return True
            return False

        def check_if_in_header(htmlParser, h_i, string):
            headers = htmlParser.find_all(h_i)
            if (type(headers) == type(None)) or (len(headers) == 0):
                return False
            for h in headers:
                if string.lower() in h.text.lower():
                    return True
            return False

        # dictionary for score
        score_dict = {'title': 0.07, 'h1': 0.06, 'h2': 0.05, 'h3': 0.04,
                      'h4': 0.03, 'h5': 0.02, 'h6': 0.01}
        paragraphs = ""
        paragraph_tags = htmlParse.find_all('p')
        for p in paragraph_tags:
            paragraphs += str(p.text).lower()

        # check for a valid paragraph. if not valid - uses title as a paragraph.
        if len(paragraphs) <= 5 or re.search('[a-zA-Z]', paragraphs) is None:
            paragraphs = title.text

        # 'yake' properties
        language = "en"
        max_ngram_size = 2
        deduplication_threshold = 0.9
        numOfKeywords = 20
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                    top=numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(paragraphs)
        res_list = []

        # the algorithm core
        for kw in keywords:
            new_score = kw[1]
            if check_if_in_title(title.text.lower(), str(kw[0]).lower()):
                new_score = kw[1] * (1 - score_dict['title'])
            for i in range(1, 7):
                if check_if_in_header(htmlParse, 'h' + str(i), str(kw[0]).lower()):
                    new_score = kw[1] * (1 - score_dict['h' + str(i)])
            new_tuple = (kw[0], new_score)
            res_list.append(new_tuple)

        def key_func(tupleKey):
            return tupleKey[1]

        res_list.sort(key=key_func)
        res = []
        for w in res_list:
            res.append(w[0])

        return response.set_keywords(res)

    def scrap_page(self, url):
        """
        purpose: receive URL, check if valid and returns extracted info: title, description, keywords.
        :param url: landing page url
        :return: dictionary with title, description and list of keywords
        """
        if url is None or url == "":
            return {"title": "",
                    "description": "",
                    "keywords": []}
        htmlParse, e = self.scan_landing_page(url)

        # if URL not valid, returns an appropriate message
        if htmlParse is None:
            return {"title": "can't open the url",
                    "description": "can't open the url",
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
