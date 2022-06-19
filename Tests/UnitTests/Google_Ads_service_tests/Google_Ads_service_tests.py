import unittest
from unittest import TestCase
import GoogleAdsService.CampaignManagement as cm


class Test(TestCase):
    def setUp(self):
        self.customer_id = "5103537456"
        self.campaign_id = "17366135188"
        self.ad_group_id = "1"

    def test_create_new_campaign_valid(self):
        res = cm.create_new_campaign(self.customer_id, 10, "test name 1", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH", "CLICKS",
                                     ["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
        status = res.get('status')
        id = res.get('body').get('id')
        cm.delete_campaign(self.customer_id,id)
        self.assertEqual(status, 200)
        self.assertNotEqual(id, "")

    #todo add more invalid?
    def test_create_new_campaign_invalid_customer_id(self):
        res = cm.create_new_campaign("-1", 10, "test name 1", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH", "CLICKS",
                                     ["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_get_campaign_by_id_valid(self):
        res = cm.get_campaign_by_id(self.customer_id, self.campaign_id)
        status = res.get('status')
        camp = res.get('body').get('campaigns').get('data')
        self.assertEqual(status, 200)
        self.assertEqual(len(camp) > 0, True)

    def test_get_campaign_by_id_invalid(self):
        res = cm.get_campaign_by_id("-1", self.campaign_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)

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
        res = cm.delete_campaign(self.customer_id, "-1")
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_create_new_ad_group_valid(self):
      res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad", "PAUSED", 1)
      ad_group_id=res.get('body').get('ad_group_id')
      status = res.get('status')
      cm.delete_ad_group(self.customer_id, ad_group_id)
      self.assertEqual(status, 200)



    #todo check if name int?
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
      self.assertNotEqual(status, 200)

    # todo check if need to treat
    # def test_create_new_ad_group_noneBid(self):
    #     res = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_name","PAUSED", None)
    #     status = res.get('status')
    #     self.assertNotEqual(status, 200)

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
      self.assertEqual(status, 200)
      res = cm.get_all_ad_groups(self.customer_id, None)
      status = res.get('status')
      self.assertNotEqual(status, 200)



    def test_delete_ad_group_valid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_ad_group_tmp", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      res = cm.delete_ad_group(self.customer_id, ad_group_id)
      status = res.get('status')
      self.assertEqual(status, 200)

    def test_add_keyword_valid(self):
        res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_1", "PAUSED", 1)
        ad_group_id=res_1.get('body').get('ad_group_id')
        res = cm.add_keyword(self.customer_id, ad_group_id, "text")
        status = res.get('status')
        cm.delete_keyword(self.customer_id, ad_group_id)
        cm.delete_ad_group(self.customer_id, ad_group_id)
        self.assertEqual(status, 200)

    # todo complete text null? what is invalid?
    def test_add_keyword_invalid(self):
        res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_2", "PAUSED", 1)
        ad_group_id=res_1.get('body').get('ad_group_id')
        res = cm.add_keyword(self.customer_id, "-1", "text")
        status = res.get('status')
        cm.delete_ad_group(self.customer_id, ad_group_id)
        self.assertNotEqual(status, 200)

    def test_get_keywords_valid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_3", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      cm.add_keyword(self.customer_id, ad_group_id, "text") #todo text? what to insert
      res = cm.get_keywords(self.customer_id, ad_group_id)
      status = res.get('status')
      cm.delete_keyword(self.customer_id, ad_group_id)
      cm.delete_ad_group(self.customer_id,ad_group_id)
      self.assertEqual(status, 200)

    def test_get_keywords_invalid(self):
        res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_4", "PAUSED", 1)
        id_group = res_1.get('body').get('ad_group_id')

        res = cm.get_keywords(self.customer_id, "-1")
        status = res.get('status')
        self.assertNotEqual(status, 200) #todo Not equal?

        cm.add_keyword(self.customer_id, id_group, "text")
        res = cm.get_keywords(self.customer_id, "-1") #todo Not equal?
        status = res.get('status')
        cm.delete_keyword(self.customer_id, id_group)
        cm.delete_ad_group(self.customer_id, id_group)
        self.assertNotEqual(status, 200)

    def test_delete_keyword_valid(self):
      res_1 = cm.create_new_ad_group(self.customer_id, self.campaign_id, "test_key_2", "PAUSED", 1)
      ad_group_id = res_1.get('body').get('ad_group_id')
      res_2 = cm.add_keyword(self.customer_id, ad_group_id, "text") #todo text?
      keyword_id = res_2.get('body').get('keyword_id')
      res = cm.delete_keyword(self.customer_id, ad_group_id, keyword_id) #todo keyword = criation?
      status = res.get('status')
      self.assertEqual(status, 200)

    #todo check params - all ad
    def test_create_new_responsive_search_ad_valid(self):
      res = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id, ["headlines_texts"], ["descriptions_texts"], "final_url", pinned_text=None)
      status = res.get('status')
      ad_id = res.get('body').get('ad_id')
      self.assertEqual(status, 200)
      cm.delete_ad(self.customer_id,self.ad_group_id,ad_id)

    def test_get_all_responsive_search_ads_valid(self):
        #res=cm.create_new_responsive_search_ad() todo add?
        res = cm.get_all_responsive_search_ads(self.customer_id, "ad_group_id")
        status = res.get('status')
        # = res.get('body').get('data')
        self.assertEqual(status, 200)

    #todo check, check params - all ad
    def test_delete_ad_valid(self):
        res_1 = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id, "headlines_texts",
                                                 "descriptions_texts", "final_url", pinned_text=None)
        ad_id = res_1.get('body').get('ad_id')
        res = cm.delete_ad(self.customer_id, self.ad_group_id, ad_id)
        status = res.get('status')
        self.assertEqual(status, 200)

    def test_delete_ad_invalid(self):
        res_1 = cm.create_new_responsive_search_ad(self.customer_id, self.ad_group_id, "headlines_texts",
                                                   "descriptions_texts", "final_url", pinned_text=None)
        ad_id = res_1.get('body').get('ad_id')
        res = cm.delete_ad("-1", self.ad_group_id, ad_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.delete_ad(self.customer_id, "-1", ad_id)
        status = res.get('status')
        self.assertNotEqual(status, 200)
        res = cm.delete_ad(self.customer_id, self.ad_group_id, "-1")
        status = res.get('status')
        self.assertNotEqual(status, 200)
        cm.delete_ad(self.customer_id, self.ad_group_id, ad_id)

    def test_get_statistics_to_csv_valid(self):
        res=cm.get_statistics_to_csv(self.customer_id, "output_file", "write_headers", "period")
        status = res.get('status')
        self.assertEqual(status, 200)

    #todo add more invalid?
    def test_get_statistics_to_csv_invalid(self):
        res=cm.get_statistics_to_csv("-1", "output_file", "write_headers", "period")
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_get_keyword_stats_valid(self):
        res=cm.get_keyword_stats(self.customer_id, "output_file", "write_headers")
        status = res.get('status')
        self.assertEqual(status, 200)

    # todo add more invalid?
    def test_get_keyword_stats_invalid(self):
        res=cm.get_keyword_stats("-1", "output_file", "write_headers")
        status = res.get('status')
        self.assertNotEqual(status, 200)




    #todo which location

    # def test__create_location_op_valid(self):
    #     res=cm._create_location_op(self.customer_id, self.campaign_id, "locations")
    #
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