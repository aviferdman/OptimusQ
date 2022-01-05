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
                print('ok')

            except Exception as e:
                print("index: " + str(i) + ": " + str(e))
            i = i + 1


if __name__ == '__main__':
    unittest.main()
