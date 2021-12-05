import urllib.request
import yake as yake
from bs4 import BeautifulSoup


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
        # opening the url for reading
        html = urllib.request.urlopen(url)

        # parsing the html file
        htmlParse = BeautifulSoup(html, 'lxml')
        title = htmlParse.find('title')
        return htmlParse, title

    def extract_keywords_from_landing_page(self, url):
        """
        purpose: extract keywords from  a landing page.
        :param url: landing page url
        :return: list of keywords
        """
        htmlParse, title = self.scan_landing_page(url)

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
        # print(paragraphs)

        kw_extractor = yake.KeywordExtractor()
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
        count = 0
        for w in res_list:
            if count == 5:
                break
            count += 1
            res.append(w[0])

        return res

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

    def recommend_n_photos_by_keywords(self, image_repos, keywords, n):
        """
        purpose: returns the most n relevant photos for the given keywords, from image_repos
         repositories.
        :param n: number of photos to be recommended
        :param keywords: keywords for choosing the photos
        :param image_repos: a list of image repositories API's to search from
        :return: n most relevant photos
        """
        pass

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
