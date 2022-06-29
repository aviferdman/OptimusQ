import unittest
from unittest import TestCase
import GoogleAdsService.CampaignManagement as cm


class Test(TestCase):
    def setUp(self):
        self.customer_id = "5103537456"
        self.campaign_id = "17538158096"
        self.ad_group_id = "134777639741"

    def test_create_new_campaign_valid(self):
        res = cm.create_new_campaign(self.customer_id, 10, "test_new_campaign", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH", "CLICKS",
                                     ["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
        status = res.get('status')
        id = res.get('body').get('id')
        cm.delete_campaign(self.customer_id,id)
        self.assertEqual(status, 200)
        self.assertNotEqual(id, "")

    #todo add more invalid?

    # def test_create_new_campaign_invalid_customer_id(self):
    #     res = cm.create_new_campaign("-1", 10, "test_new_campaign_invalid", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH", "CLICKS",
    #                                  ["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
    #     status = res.get('status')
    #     self.assertNotEqual(status, 200)

    def test_get_campaign_by_id_valid(self):
        res = cm.get_campaign_by_id(self.customer_id, self.campaign_id)
        status = res.get('status')
        camp = res.get('body').get('campaigns').get('data')
        self.assertEqual(status, 200)
        self.assertEqual(len(camp) > 0, True)

    #todo fix id not valid?
    def test_get_campaign_by_id_invalid(self):
        res = cm.get_campaign_by_id("-1", self.campaign_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        # res = cm.get_campaign_by_id(self.customer_id, 1)
        # status = res.get('status')
        # self.assertNotEqual(status, 200)

    def test_get_all_campaigns_valid(self):
        res = cm.get_all_campaigns(self.customer_id)
        status = res.get('status')
        body = res.get('body').get('campaigns').get('data')
        self.assertEqual(len(body) > 0, True)
        self.assertEqual(status, 200)

    def test_get_all_campaigns_invalid_customer_id(self):
        res = cm.get_all_campaigns("-1")
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_campaign_valid(self):
        res_1 = cm.create_new_campaign(self.customer_id, 10, "test del", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH",
                                     "CLICKS",["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
        id_to_del = res_1.get('body').get('id')
        res = cm.delete_campaign(self.customer_id, id_to_del)
        status = res.get('status')
        self.assertEqual(status, 200)

    def test_delete_campaign_invalid_campaignId(self):
        res = cm.delete_campaign("-1",self.campaign_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.delete_campaign(self.customer_id, "-1")
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_create_new_ad_group_valid(self):
      res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad", "PAUSED", 1)
      ad_group_id=res.get('body').get('ad_group_id')
      status = res.get('status')
      cm.delete_ad_group(self.customer_id, ad_group_id)
      self.assertEqual(status, 200)

    #todo fix name int
    def test_create_new_ad_group_invalid_name(self):
      tmp_res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad_0", "PAUSED", 1)
      ad_group_id = tmp_res.get('body').get('ad_group_id')
      res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad_0", "PAUSED", 1)
      status = res.get('status')
      cm.delete_ad_group(self.customer_id, ad_group_id)
      self.assertNotEqual(status, 200)
      res = cm.create_new_ad_group(self.customer_id, self.campaign_id, None, "PAUSED", 1)
      status = res.get('status')
      self.assertNotEqual(status, 200)

    def test_create_new_ad_group_noneId(self):
        res = cm.create_new_ad_group(None, self.campaign_id, "None", "PAUSED", 1)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.create_new_ad_group(self.customer_id, None, "None", "PAUSED", 1)
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_create_new_ad_group_noneStatus(self):
      res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad_status", None, 1)
      status = res.get('status')
      ad_group_id = res.get('body').get('ad_group_id')
      cm.delete_ad_group(self.customer_id, ad_group_id)
      self.assertEqual(status, 200)

    # todo fix bid not int
    # def test_create_new_ad_group_noneBid(self):
    #     res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_name","PAUSED", None)
    #     status = res.get('status')
    #     self.assertNotEqual(status, 200)

    def test_get_ad_groups_valid(self):
      res=cm.get_ad_group_by_id(self.customer_id, self.ad_group_id)
      status = res.get('status')
      self.assertEqual(status, 200)

    #todo return 200 - empty
    def test_get_ad_groups_invalid(self):
      res=cm.get_ad_group_by_id("-1", self.ad_group_id)
      status = res.get('status')
      self.assertNotEqual(status, 200)
      res=cm.get_ad_group_by_id(self.customer_id, 1)
      status = res.get('status')
      campaign = res.get('body')
      self.assertEqual(len(campaign) == 0, True)
      self.assertEqual(status, 200)

    def test_get_all_ad_groups_valid(self):
      res = cm.get_all_ad_groups(self.customer_id, self.campaign_id)
      status = res.get('status')
      self.assertEqual(status, 200)

    def test_get_all_ad_groups_invalid_customer_id(self):
      res = cm.get_all_ad_groups("-1", self.campaign_id)
      status = res.get('status')
      self.assertNotEqual(status, 200)
      res = cm.get_all_ad_groups(None, self.campaign_id)
      status = res.get('status')
      self.assertNotEqual(status, 200)

    def test_get_all_ad_groups_invalid_campaign_id(self):
      res = cm.get_all_ad_groups(self.customer_id, "-1")
      status = res.get('status')
      campaign=res.get('body').get('data')
      self.assertEqual(len(campaign) > 0, False)
      self.assertEqual(status, 200)
      res = cm.get_all_ad_groups(self.customer_id, None)
      status = res.get('status')
      campaign = res.get('body').get('data')
      self.assertEqual(len(campaign) > 0, True)
      self.assertEqual(status, 200)

    def test_delete_ad_group_valid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad_group_tmp", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      res = cm.delete_ad_group(self.customer_id, ad_group_id)
      status = res.get('status')
      self.assertEqual(status, 200)

    def test_delete_ad_group_invalid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad_group_tmp", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      res = cm.delete_ad_group("-1", ad_group_id)
      status = res.get('status')
      self.assertNotEqual(status, 200)
      res = cm.delete_ad_group(self.customer_id, 1)
      status = res.get('status')
      self.assertNotEqual(status, 200)
      cm.delete_ad_group(self.customer_id, ad_group_id)

    def test_add_keyword_valid(self):
        res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_1", "PAUSED", 1)
        ad_group_id=res_1.get('body').get('ad_group_id')
        res = cm.add_keyword(self.customer_id, ad_group_id, "keyword")
        status = res.get('status')
        creation_id=res.get('body').get('keyword_id')
        cm.delete_keyword(self.customer_id, ad_group_id,creation_id)
        cm.delete_ad_group(self.customer_id, ad_group_id)
        self.assertEqual(status, 200)

    def test_add_keyword_invalid(self):
        res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_2", "PAUSED", 1)
        ad_group_id=res_1.get('body').get('ad_group_id')
        res = cm.add_keyword(self.customer_id, "-1", "keyword")
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.add_keyword(self.customer_id, ad_group_id, None)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        cm.delete_ad_group(self.customer_id, ad_group_id)

    def test_get_keywords_valid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_3", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      res_2=cm.add_keyword(self.customer_id, ad_group_id, "keyword")
      creation_id=res_2.get('body').get('keyword_id')
      res = cm.get_keywords(self.customer_id, ad_group_id)
      status = res.get('status')
      keywords = res.get('body').get('data')
      cm.delete_keyword(self.customer_id, ad_group_id, creation_id)
      cm.delete_ad_group(self.customer_id, ad_group_id)
      self.assertEqual(len(keywords) > 0, True)
      self.assertEqual(status, 200)
      res = cm.get_keywords(self.customer_id, "-1")
      status = res.get('status')
      self.assertEqual(status, 200)

    # #todo fix costumer id
    # def test_get_keywords_invalid(self):
    #     res = cm.get_keywords(1, 1)
    #     status = res.get('status')
    #     self.assertEqual(status, 200)

    def test_delete_keyword_valid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_5", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      res_2 = cm.add_keyword(self.customer_id, ad_group_id, "keyword")
      keyword_id = res_2.get('body').get('keyword_id')
      res = cm.delete_keyword(self.customer_id, ad_group_id, keyword_id)
      status = res.get('status')
      cm.delete_ad_group(self.customer_id,ad_group_id)
      self.assertEqual(status, 200)

    def test_create_new_responsive_search_ad_valid(self):
      res = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id, ["headlines_1","headlines_2","headlines_3"], ["descriptions_1","descriptions_2"], "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
      status = res.get('status')
      ad_id = res.get('body').get('ad_id')
      self.assertEqual(status, 200)
      cm.delete_ad(self.customer_id,self.ad_group_id,ad_id)

    #todo fix costumer id int
    def test_create_new_responsive_search_ad_invalid(self):
      #2 headlines inside 3
      res = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id, ["headlines_1","headlines_2"], ["descriptions_1","descriptions_2"], "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
      status = res.get('status')
      self.assertNotEqual(status, 200)

      #1 descriptions inside 2
      res = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id, ["headlines_1", "headlines_2","headlines_3"],
                                               ["descriptions_1"],
                                               "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
      status = res.get('status')
      self.assertNotEqual(status, 200)

      # url invalid
      res = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id,
                                               ["headlines_1", "headlines_2", "headlines_3"],
                                               ["descriptions_1", "descriptions_2"],
                                               "azurewebsites.net/", pinned_text=None)
      status = res.get('status')
      self.assertNotEqual(status, 200)

      # ad_group id invalid
      res = cm.create_new_responsive_search_ad(self.customer_id, 1,
                                               ["headlines_1", "headlines_2", "headlines_3"],
                                               ["descriptions_1", "descriptions_2"],
                                               "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
      status = res.get('status')
      self.assertNotEqual(status, 200)

      # custumer id invalid
      res = cm.create_new_responsive_search_ad("-1", self.ad_group_id,
                                               ["headlines_1", "headlines_2", "headlines_3"],
                                               ["descriptions_1", "descriptions_2"],
                                               "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
      status = res.get('status')
      self.assertNotEqual(status, 200)

    def test_get_all_responsive_search_ad_valid(self):
        res = cm.get_all_responsive_search_ads(self.customer_id, self.ad_group_id)
        status = res.get('status')
        self.assertEqual(status, 200)

    def test_get_all_responsive_search_ad_invalid(self):
        res = cm.get_all_responsive_search_ads("-1", self.ad_group_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.get_all_responsive_search_ads(self.customer_id, 1)
        status = res.get('status')
        ads=res.get('body').get('data')
        self.assertEqual(status, 200)
        self.assertEqual(len(ads)==0, True)

    def test_delete_ad_valid(self):
        res_1 = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id,
                                                 ["headlines_1", "headlines_2", "headlines_3"],
                                                 ["descriptions_1", "descriptions_2"],
                                                 "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
        ad_id = res_1.get('body').get('ad_id')
        res = cm.delete_ad(self.customer_id, self.ad_group_id, ad_id)
        status = res.get('status')
        self.assertEqual(status, 200)

    #todo check costumer id int
    def test_delete_ad_invalid(self):
        res_1 = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id,
                                                   ["headlines_1", "headlines_2", "headlines_3"],
                                                   ["descriptions_1", "descriptions_2"],
                                                   "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
        ad_id = res_1.get('body').get('ad_id')
        res = cm.delete_ad("-1", self.ad_group_id, ad_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.delete_ad(self.customer_id, 1, ad_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.delete_ad(self.customer_id, self.ad_group_id, "-1")
        status = res.get('status')
        self.assertNotEqual(status, 200)
        cm.delete_ad(self.customer_id, self.ad_group_id, ad_id)

    def test_get_responsive_search_ad_invalid(self):
        res_1 = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id,
                                                 ["headlines_1", "headlines_2", "headlines_3"],
                                                 ["descriptions_1", "descriptions_2"],
                                                 "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
        ad_id = res_1.get('body').get('ad_id')
        res = cm.get_responsive_search_ad_by_id(self.customer_id, ad_id)
        status = res.get('status')
        ads = res.get('body').get('data')
        self.assertEqual(len(ads) > 0, True)
        self.assertEqual(status, 200)
        cm.delete_ad(self.customer_id, self.ad_group_id, ad_id)

    def test_get_responsive_search_ad_invalid(self):
        res_1 = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id,
                                                   ["headlines_1", "headlines_2", "headlines_3"],
                                                   ["descriptions_1", "descriptions_2"],
                                                   "https://scannerwebapp.azurewebsites.net/", pinned_text=None)
        ad_id = res_1.get('body').get('ad_id')
        res = cm.get_responsive_search_ad_by_id("-1", ad_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        cm.delete_ad(self.customer_id, self.ad_group_id, ad_id)
        res = cm.get_responsive_search_ad_by_id(self.customer_id,  "-1")
        status = res.get('status')
        self.assertNotEqual(status, 200)


    # def test__create_location_op_valid(self):
    #      res=cm._create_location_op(self.customer_id, self.campaign_id, "locations")

    # def test__create_age_op_valid(self):
    #     res=cm._create_age_op(self.customer_id, self.campaign_id," min_age", "max_age")
    #
    # def test__create_gender_op_valid(self):
    #     res = cm._create_gender_op("client", self.customer_id, self.campaign_id, "gender")
    #
    # def test__create_device_op_valid(self):
    #     res=cm._create_device_op("client", self.customer_id, self.campaign_id, "device_type")
    #
    # def test__create_operating_system_op_valid(self):
    #     res=cm._create_operating_system_op("client", self.customer_id, self.campaign_id)
    #
    # def test__create_user_interest_op_valid(self):
    #     res=cm._create_user_interest_op("client", self.customer_id, self.campaign_id, "interest")






    # def test_get_statistics_to_csv_valid(self):
    #     res=cm.get_statistics_to_csv(self.customer_id, "output_file", "write_headers", "period")
    #     status = res.get('status')
    #     self.assertEqual(status, 200)
    #
    # def test_get_statistics_to_csv_invalid(self):
    #     res=cm.get_statistics_to_csv("-1", "output_file", "write_headers", "period")
    #     status = res.get('status')
    #     self.assertNotEqual(status, 200)

    # def test_get_keyword_stats_valid(self):
    #     res=cm.get_keyword_stats(self.customer_id, "output_file", "write_headers")
    #     status = res.get('status')
    #     self.assertEqual(status, 200)
    #
    #
    # def test_get_keyword_stats_invalid(self):
    #     res=cm.get_keyword_stats("-1", "output_file", "write_headers")
    #     status = res.get('status')
    #     self.assertNotEqual(status, 200)




    #todo which location

