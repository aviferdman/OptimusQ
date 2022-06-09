import unittest
from unittest import TestCase
import GoogleAdsService.CampaignManagement as cm


class Test(TestCase):
    def setUp(self):
        self.token = ""
        self.customer_id = "5103537456"


    def test_create_new_campaign_valid(self):
        res = cm.create_new_campaign(self.customer_id, 10, "test name1", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH", "CLICKS",
                                     ["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)
        self.assertNotEqual(body.get('id'), "")

    def test_create_new_campaign_invalid_customer_id(self):
        res = cm.create_new_campaign("123", 10, "test name1", 2, 4, "PAUSED", "STANDARD", "DAILY", "SEARCH",
                                     "CLICKS",
                                     ["New York"], "FEMALE", "DESKTOP", 25, 34, "Subaru")
