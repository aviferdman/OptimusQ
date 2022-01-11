import unittest
import pandas as pd

from ScanningService import recoSystem


class TestRecoSystem(unittest.TestCase):

    # create RecoSystem
    def setUp(self):
        self.reco = recoSystem.RecoSystem()

    # reads url from the valid file, for each of the urls.
    # asserts the return is not "cant open the url"
    def test_valid_url(self):
        i = 0
        data = pd.read_excel(r'valid.xlsx')

        df = pd.DataFrame(data, columns=['url'])
        for d in df.values:
            try:
                dict = self.reco.scrap_page(d[0])
                title = dict['title']
                description = dict['description']
                keywords = dict['keywords']
                self.assertNotEqual(title, "cant open the url")
                self.assertNotEqual(description, "cant open the url")
                self.assertNotEqual(keywords, "cant open the url")
                self.assertNotEqual(keywords, [])

            except Exception as e:
                print("index: " + str(i) + ": " + str(e))
            i = i + 1

    # reads url from the NON-valid file, for each of the urls.
    # asserts the return is "cant open the url", for each one.
    def test_problem_url(self):
        i = 0
        data = pd.read_excel(r'problem.xlsx')

        df = pd.DataFrame(data, columns=['url'])
        for d in df.values:
            try:
                dict = self.reco.scrap_page(d[0])
                title = dict['title']
                description = dict['description']
                keywords = dict['keywords']
                self.assertEqual(title, "cant open the url")
                self.assertEqual(description, "cant open the url")
                self.assertEqual(keywords, [])
                print("index: " + str(i) + ": description" + description + " title: "+ title + " keywords: ")
                print(keywords)

            except Exception as e:
                print("index: " + str(i) + ": " + str(e))
            i = i + 1

    def test_valid_with_keywords_only(self):
        url = "https://apnews.com/afs:Content:1514120141?utm_source=taboolabackfill&utm_medium=referral&tblci=GiAId4kjQ6dTOp8dg6bJwUI-8OUfgEHnD44_lOK_M8-l9iD46Eco9-Pc4r661Jts"
        dict = self.reco.scrap_page(url)
        title = dict['title']
        description = dict['description']
        keywords = dict['keywords']
        self.assertEqual(title, "")
        self.assertEqual(description, "Cannot extract description")
        self.assertNotEqual(keywords, [])

    def test_valid_with_no_description(self):
        url = "http://news.bbc.co.uk/1/hi/business/6098484.stm"
        dict = self.reco.scrap_page(url)
        title = dict['title']
        description = dict['description']
        keywords = dict['keywords']
        self.assertNotEqual(title, "")
        self.assertEqual(description, "Cannot extract description")
        self.assertNotEqual(keywords, [])

    def test_valid_with_keyword_like_title(self):
        url = "https://www.hcpcacao.org/about-hcp.html?gclid=CjwKCAiArOqOBhBmEiwAsgeLmS1PnHyasvY6NY2_Vs9QqTTLpBIDzCssxKFic_xqnNPSaKBRkxuQuBoCvhMQAvD_BwE"
        dict = self.reco.scrap_page(url)
        title = dict['title']
        description = dict['description']
        keywords = dict['keywords']
        self.assertNotEqual(title, "")
        self.assertNotEqual(description, "Cannot extract description")
        self.assertNotEqual(keywords, [])
        self.assertEqual(keywords[0], title)


if __name__ == '__main__':
    unittest.main()
