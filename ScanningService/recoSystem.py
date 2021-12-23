import re
import urllib.request

import requests
import yake as yake
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

from ScanningService.response import Response


class RecoSystem:
    def enter_landing_page_url(self):
        """
        purpose: receives a landing page url.
        :param url: landing page url
        :return: void
        """
        pass

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

    def extract_title_from_landing_page(self, url):
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
        hdr = {'User-Agent': 'Mozilla/5.0'}
        try:
            req = Request(url, headers=hdr)
            html = urlopen(req)
        except Exception as e:
            res.sign_error(e,True)
            res.set_messege("cant open the url")
            return res

        # parsing the html file
        htmlParse = BeautifulSoup(html, 'lxml')
        title = htmlParse.find('title')
        if title is None:
           res.sign_error(None,True)
           res.set_messege("Cannot extract title")
           return res
        return res.set_title(title.text)

    def extract_description_from_landing_page(self, url):
        res = Response()
        res.set_url(url)
        htmlParse, e = self.scan_landing_page(url)
        if htmlParse is None:
            res.sign_error(e, True)
            res.set_messege("cant open the url")
            return res
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

    def extract_keywords_from_landing_page(self, url):
        """
        purpose: extract keywords from  a landing page.
        :param url: landing page url
        :return: list of keywords
        """
        response= Response()
        response.set_url(url)
        htmlParse, e = self.scan_landing_page(url)
        if htmlParse is None:
            response.sign_error(e, True)
            response.set_messege("cant open the url")
            return response

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
            if len(res) < 5:
                return response.set_keywords(res)
            return response.set_keywords(response)

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
            return response.set_keywords([title.text])

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
        if url is None or url=="":
            return {"title": "",
                    "description": "",
                    "keywords": []}
        response = self.extract_title_from_landing_page(url)
        if response.is_error():
            title = response.get_messege()
        else:
            title = response.get_title()
        response = self.extract_description_from_landing_page(url)
        if response.is_error():
            description = response.get_messege()
        else:
            description = response.get_description()
        response = self.extract_keywords_from_landing_page(url)
        if response.is_error():
            keywords = []
        else:
            keywords = response.get_keywords()

        dict = {"title": title,
                "description": description,
                "keywords": keywords}

        return dict

    def add_scraping_rule(self, new_rule):
        """
        purpose: add a new rule for scraping a landing page
        :param new_rule:
        :return: void
        """
        pass

    def edit_a_scraping_rule(self, rule_id):
        """
        purpose: edit an existing scraping rule.
        :param rule_id:
        :return: void
        """
        pass

    def connect_to_image_repositories(self, image_repos):
        """
        purpose: connects to the specified image repositories.
        :param image_repos: a list of image repositories API's to connect
        :return: void
        """
        pass

    def disconnect_from_image_repositories(self, image_repos):
        """
        purpose: disconnects from the specified image repositories.
        :param image_repos: a list of image repositories API's to disconnect from
        :return: void
        """
        pass

    def parse_result(self, text):
        index1 = text.find('[')
        index2 = text.find(']')
        new_str = text[index1 + 1:index2]
        new_str = new_str.split(',')
        res = []
        for s in new_str:
            tmp = s.replace("\"", "")
            res.append(tmp)
        return res

    def recommend_n_photos_by_keywords(self, image_repos, keywords, n):
        """
        purpose: returns the most n relevant photos for the given keywords, from image_repos
         repositories.
        :param n: number of photos to be recommended
        :param keywords: keywords for choosing the photos
        :param image_repos: a list of image repositories API's to search from
        :return: n most relevant photos
        """
        res = []
        for k in keywords:
            url = f"https://optimusqbgu.azurewebsites.net/api/imageservice?stock={image_repos}&keywords={k}&maxImages={str(n)}"
            res = requests.get(url)
            list_of_images = self.parse_result(res.text)
            for p in list_of_images:
                if p:
                    res.append(p)
        return res

    def recommend_n_photos_by_landing_page(self, image_repos, landing_url, n):
        """
        purpose: scrape the landing page given in landing_url. Returns the most n relevant photos
        from image_repos, given the landing page.
         repositories.
        :param landing_url: url of a landing page
        :param n: number of photos to be recommended
        :param image_repos: a list of image repositories API's to search from
        :return: n most relevant photos
        """
        pass

    def process_image_from_a_repository(self, image):
        """
        purpose: receives an image, processes it and returns the image's metadata.
        :param image: image to be processes
        :return: metadata extracted from the image
        """
        pass

    def get_error_log(self):
        """
        purpose: returns error log
        :return: error log
        """
        pass

    def get_action_log(self):
        """
        purpose: returns action log
        :return: action log
        """
        pass
