import unittest
import pandas as pd

from ScanningService import recoSystem


class TestRecoSystem(unittest.TestCase):

    def setUp(self):
        self.reco = recoSystem.RecoSystem()

    def test_Enter_URL(self):
        result1, e1 = self.reco.scan_landing_page("https://www.bbcgoodfood.com/howto/guide/top-10-winter-drinks")
        result2, e2 = self.reco.scan_landing_page("")
        result3 = self.reco.extract_keywords_from_landing_page("http://be-intl-big-brain-in-canadas-ok.live/?honeypot&params=rif5ibpy4-M73NLOu99bE3I3JHwKqOm_eNO4H7K3HtFNjylmkmSJB9ZnSK3G7VWdt1zI1vdmm0BDkJ8Yu3D8d_QChB4Rm8ekePzho6-4inOj6cHqjxQoV28mpg6Z5QtZtwaWzJFdZsZdpH_lq0yoqzhpGofPej9EW3tiaDH5eSYb0mef7H8wtyRuazLMcuvr7MrhXdWYVLWpijqB8SxfTxS9Rs3rAGjifajfX055PaIxnxkrNP0GaYleLArt1gDL9fy0nGWj-eZ-AzqOG53E-ERvd98kSLHoQWx68fVs8TKhIQDgH3_reA1I9G5ImegAWrlIrcucvcSKwb6SFS5ztgEj5YmyJB9m7-1oQK7ODoE4lqQo8cjAioPJXZkvNJuw_WUN6kIWFxEd_WWg0iGTcKLanqtAQMA9KDmLuodcyQz4ZXbFVDnqQR3idi6gjNtu69vEIGFgF1mQ34oAq9tltYKcS7GgLh56ZEZxnZxomgD2VXNrkZ9AWu8C0E1dl8Hp3F8978Esp_-QoGhzrxcfx6pM-0PWZUSJ2KE8C1MY2P_dKJrgouZ8jnE-yaNCpu7wtW43sNCOwfbDfmoRqLeqZgh_zSTgcyW08f1aLg97lfWbvn6CZInoo5CpT88Xof285ovzjNOvP-HE44OccL1BEa2MAih6oJ8M3h2o_oCdKGxAACjtfhFZSJ0EkiHC9CjlvlN28yZCCat1hwYbwhP-X8-KqvfhQBgDW1HQzQn0BPaIBbPvHoKxiut2aoi9M05x5HMLgC9jCHh5mZAf_6F2Mdc_smkT_PY079LL5Em9giKOgM0g19mD5dgXvNFLjbK1-Bo0v-JkGGoc7huiBUm-bTfvD2d4GOhOvUa0tb9i5a4He7Ddk0aM7Ce150Yx0pfYoKd6tbG_G7n7T7CPKIMDmk1MJcYiHwqTsGGhKpqp2Mgk7EVCx4z-VvAkc_3FY3-3GS7TLJ7KYjyN5AxdCFvIURCwJNyALOsC6DV87fd8lUJ-HBLfwC1kRcIHo7cCLvuzhN0atkFPEO6wTc1N-UIAXLhJ6g_bdNuQT1j63NKBF_VJMmEkaTM5CE4pMZGzr_I_4TNH4VZeUXzZg0KjNSKEkOCdey9q7WzFyq5hIh2UArxQ7YzCgLHunj_2O0RMzYZwda5ZdDW_RmTUAhturkByD3n92I-qSd_T2yNEbWxn50yIz0h4S51d9O9I1cXfmxnP8O0ghPLHsk7G_PQAvmZkSmSD9yVxAmoIyOmuyDIJIoc5myxUsSBnxA4OqOeju6HMIXSt2QpslNaxa1oLzc3VgUe5YCdeOtK48aXdcuOY-0bpOR8aOdCP5EbmcQ1u7V9seFBHR3WezCJtyuqYtV5_nLQ-nXQQu_6iKuwOYdoKlGIliqYCi42fyULTBoSHEO6vIVMIR-4-HV6JkR6SWMSSYCdTI1URPcKCuUr67fDKs4fSN1wiDfkkC8Yp4DJ1HqqgLGRDxaAHM7cGMhkNjNSYfqgCMjk3d-S0Otbdt9pgeSOuyk1v0iBiNcNjtIf_06NuXbjXAZe3kozUx6exJ1eqkoWjEbwHg9unqTbjpQ01gCvpGUNlAwbMEYQftJfPnzvy29kB4EgcQMq1sZNcO2wvhtWSaPKW1CcjsDxrseJXuQLYd05p4jpbPcR3vzvndGYFnm-n3A45gBm7Nnt0wXGVljLOrjnGXB5tCAvjVGudx-s-nWub7nIUvrprApDmZqJ3YBPAlHkL_LDcazNwAAUZL-Lvz0axbWs6S9pkbwvhnYlIq7tkCy_7pMiMHMVDOkCcCsaVvBhoguDYLyU")
        self.assertEqual(e1, "Success")
        self.assertNotEqual(e2, "Success")
        self.assertEqual(result3[0], "Exception: Cannot Access url")

        # self.assertRaises(ValueError, reco.scan_landing_page, reco, "")
        # with self.assertRaises(ValueError):
        #     reco.scan_landing_page(reco, "")


    def test_valid_url(self):
        i = 0
        data = pd.read_excel(r'valid.xlsx')
        # data["title"] = ""
        # data["description"] = ""
        # data["keywords"] = ""

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
                # data['title'].iloc[i] = dict['title']
                # data['description'].iloc[i] = dict['description']
                # data['keywords'].iloc[i] = dict['keywords']
                # data.to_excel("valid.xlsx", index=False)
            except Exception as e:
                print("index: " + str(i) + ": " + str(e))
            i = i + 1

        # #check
        # values = pd.DataFrame(data, columns=['title', 'description', 'keywords'])
        # for v in values.values:
        #     for val in v:
        #         print(val)
        #         self.assertNotEqual(val, "cant open the url")
        #

if __name__ == '__main__':
    unittest.main()
