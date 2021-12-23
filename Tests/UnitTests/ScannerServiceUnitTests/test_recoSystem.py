import unittest
import pandas as pd

from ScanningService import recoSystem


class TestRecoSystem(unittest.TestCase):

    def setUp(self):
        self.reco = recoSystem.RecoSystem()


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
                self.assertNotEqual(keywords, "Cannot extract keywords")

            except Exception as e:
                print("index: " + str(i) + ": " + str(e))
            i = i + 1

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
                self.assertEqual(keywords, "[]")

            except Exception as e:
                print("index: " + str(i) + ": " + str(e))
            i = i + 1


if __name__ == '__main__':
    unittest.main()
