import unittest
from unittest import TestCase
import FacebookService.MarketingManagement as mm
from DataBaseService.main import DataBaseController

class Test(TestCase):
    def setUp(self):
        self.db = DataBaseController()
        self.token = self.db.getAccessTokenByUserId('sandbox_token')
        self.ad_account = '1107831820072468'
        self.campaign = '120330000357827313'
        self.adset = '120330000357832413'
        self.img_hash = '49904f214677e640c43989e44cfbe927'
        self.ad_creative = '120330000357828413'
        self.ad1 = '120330000357835013'

    def test_create_new_campaign_valid(self):
        res = mm.create_new_campaign(self.token, self.ad_account, "test name1", "LINK_CLICKS")
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)
        self.assertNotEqual(body.get('id'), "")

    def test_create_new_campaign_invalid_token(self):
        res = mm.create_new_campaign('abc', self.ad_account, "test name1", "LINK_CLICKS")
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_new_campaign_invalid_ad_account(self):
        res = mm.create_new_campaign(self.token, 'aa', "test name1", "LINK_CLICKS")
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_campaign_by_id_valid(self):
        res = mm.get_campaign_by_id(self.token, self.campaign)
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(body.get('id'), self.campaign)
        self.assertEqual(body.get('name'), 'sandBox campaign1')

    def test_get_campaign_by_id_invalid_campaign_id(self):
        res = mm.get_campaign_by_id(self.token, '-1')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_campaign_by_id_invalid_token(self):
        res = mm.get_campaign_by_id('-1', self.campaign)
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)


    def test_get_all_campaigns_valid(self):
        res = mm.get_all_campaigns(self.token, self.ad_account)
        status = res.get('status')
        body = res.get('body').get('campaigns').get('data')
        self.assertEqual(len(body) > 0, True)

    def test_get_all_campaigns_invalid_token(self):
        res = mm.get_all_campaigns('-1', self.ad_account)
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_all_campaigns_invalid_ad_account(self):
        res = mm.get_all_campaigns(self.token, '-1')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_new_ad_set_valid(self):
        res = mm.create_new_ad_set(self.token, self.ad_account, 'adSet name', self.campaign)
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)
        self.assertNotEqual(body.get('id'), "")

    def test_create_new_ad_set_invalid_optimization_goal(self):
        res = mm.create_new_ad_set(self.token, self.ad_account, 'adSet name', self.campaign, '1000', 'No Opt Goal')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_new_ad_set_invalid_daily_budget(self):
        res = mm.create_new_ad_set(self.token, self.ad_account, 'adSet name', self.campaign, '-1')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_new_ad_set_invalid_token(self):
        res = mm.create_new_ad_set('-1', self.ad_account, 'adSet name', self.campaign)
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)


    def test_get_all_ad_sets_by_campaign_valid(self):
        res = mm.get_all_ad_sets_by_campaign(self.token, self.campaign)
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)
        self.assertEqual(len(body.get('data')) > 0, True)

    def test_get_all_ad_sets_by_campaign_invalid_token(self):
        res = mm.get_all_ad_sets_by_campaign('-1', self.campaign)
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_all_ad_sets_by_campaign_invalid_campaign_id(self):
        res = mm.get_all_ad_sets_by_campaign(self.token, '-1')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_all_ad_creatives_valid(self):
        res = mm.get_all_ad_creatives(self.token, self.ad_account)
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)
        self.assertEqual(len(body.get('data')) > 0, True)

    def test_get_all_ad_creatives_invalid_token(self):
        res = mm.get_all_ad_creatives('-1', self.ad_account)
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_all_ad_creatives_invalid_campaign(self):
        res = mm.get_all_ad_creatives(self.token, '-1')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)


    def test_upload_image_by_url_valid(self):
        res = mm.upload_image_by_url(self.token, self.ad_account, 'https://pixabay.com/get/g79584b6a31f1adc4b994b0a7dd15abeedd66b11dcf7155036476a352c59186650cadc37a51d62efac9ecd6d082aaf4018675560472b4454c21b5fab81724d505_640.jpg')
        status = res.get('status')
        body = res.get('body').get('images').get('bytes')
        self.assertEqual(status, 200)
        self.assertNotEqual(body.get('hash'), '')

    def test_upload_image_by_url_invalid_url(self):
        res = mm.upload_image_by_url(self.token, self.ad_account, 'hINVALIDURLttps://pixabay.com/get/g79584b6a31f1adc4b994b0a7dd15abeedd66b11dcf7155036476a352c59186650cadc37a51d62efac9ecd6d082aaf4018675560472b4454c21b5fab81724d505_640.jpg')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_upload_image_by_url_invalid_token(self):
        res = mm.upload_image_by_url('-1', self.ad_account, 'https://pixabay.com/get/g79584b6a31f1adc4b994b0a7dd15abeedd66b11dcf7155036476a352c59186650cadc37a51d62efac9ecd6d082aaf4018675560472b4454c21b5fab81724d505_640.jpg')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_ad_creative_valid(self):
        res = mm.create_ad_creative(self.token, 'ad creative name', '49904f214677e640c43989e44cfbe927', self.ad_account,
                                     'oq.com', 'msg')
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)

    def test_create_ad_creative_invalid_img_hash(self):
        res = mm.create_ad_creative(self.token, 'ad creative name', '-1', self.ad_account,
                                     'oq.com', 'msg')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_ad_creative_invalid_token(self):
        res = mm.create_ad_creative('-1', 'ad creative name', '49904f214677e640c43989e44cfbe927', self.ad_account,
                                     'oq.com', 'msg')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)


    def test_create_ad_valid(self):
        res = mm.create_ad(self.token, self.ad_account, 'ad name', '120330000357832413', '120330000357828413', 'ACTIVE')
        status = res.get('status')
        body = res.get('body')
        self.assertEqual(status, 200)

    def test_create_ad_invalid_ad_status(self):
        res = mm.create_ad(self.token, self.ad_account, 'ad name', '120330000357832413', '120330000357828413', 'Unknown Status!')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_ad_invalid_token(self):
        res = mm.create_ad('-1', self.ad_account, 'ad name', '120330000357832413', '120330000357828413', 'ACTIVE')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_ad_invalid_creative_id(self):
        res = mm.create_ad(self.token, self.ad_account, 'ad name', '120330000357832413', '-1', 'ACTIVE')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_create_ad_invalid_adset_id(self):
        res = mm.create_ad(self.token, self.ad_account, 'ad name', '-1', '120330000357828413', 'ACTIVE')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_all_ads_by_adSet_id_valid(self):
        res = mm.get_all_ads_by_adSet_id(self.token, '120330000357832413')
        status = res.get('status')
        body = res.get('body').get('data')
        self.assertEqual(status, 200)
        self.assertEqual(len(body) > 0, True)

    def test_get_all_ads_by_adSet_id_invalid_token(self):
        res = mm.get_all_ads_by_adSet_id('-1', '120330000357832413')
        status = res.get('status')
        body = res.get('body').get('data')
        self.assertNotEqual(status, 200)

    def test_get_all_ads_by_adSet_id_invalid_adset_id(self):
        res = mm.get_all_ads_by_adSet_id(self.token, '-1')
        status = res.get('status')
        body = res.get('body').get('data')
        self.assertNotEqual(status, 200)


    def test_get_ad_preview_valid_with_default_ad_format(self):
        res = mm.get_ad_preview(self.token, '120330000357835013')
        status = res.get('status')
        body = res.get('body').get('data')[0].get('body')
        self.assertEqual(status, 200)
        self.assertEqual("<iframe src" in body, True)

    def test_get_ad_preview_valid_with_ad_format_MOBILE_FEED_STANDARD(self):
        res = mm.get_ad_preview(self.token, '120330000357835013', 'MOBILE_FEED_STANDARD')
        status = res.get('status')
        body = res.get('body').get('data')[0].get('body')
        self.assertEqual(status, 200)
        self.assertEqual("<iframe src" in body, True)

    def test_get_ad_preview_valid_with_ad_format_FACEBOOK_STORY_MOBILE(self):
        res = mm.get_ad_preview(self.token, '120330000357835013', 'FACEBOOK_STORY_MOBILE')
        status = res.get('status')
        body = res.get('body').get('data')[0].get('body')
        self.assertEqual(status, 200)
        self.assertEqual("<iframe src" in body, True)

    def test_get_ad_preview_invalid_ad_format(self):
        res = mm.get_ad_preview(self.token, '120330000357835013', 'an invalid_ad_format')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_ad_preview_invalid_ad_id(self):
        res = mm.get_ad_preview(self.token, '-1')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_get_ad_preview_invalid_token(self):
        res = mm.get_ad_preview('-1', '120330000357835013')
        status = res.get('status')
        body = res.get('body')
        self.assertNotEqual(status, 200)

    def test_delete_campaign_valid(self):
        res = mm.create_new_campaign(self.token, self.ad_account, "camp to delete", "LINK_CLICKS")
        body = res.get('body')
        camp_id = body.get('id')
        res = mm.delete_campaign(self.token, camp_id)
        status = res.get('status')
        body = res.get('body').get('success')
        self.assertEqual(status, 200)
        self.assertEqual(body, True)

    def test_delete_campaign_invalid_token(self):
        res = mm.delete_campaign('-1', self.campaign)
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_campaign_invalid_campaign_id(self):
        res = mm.delete_campaign(self.token, '-1')
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_ad_set_valid(self):
        res = mm.create_new_ad_set(self.token, self.ad_account, 'adSet name', self.campaign)
        body = res.get('body')
        adset_id = body.get('id')
        res = mm.delete_adSet(self.token, adset_id)
        status = res.get('status')
        body = res.get('body').get('success')
        self.assertEqual(status, 200)
        self.assertEqual(body, True)

    def test_delete_adset_invalid_token(self):
        res = mm.delete_adSet('-1', self.adset)
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_adset_invalid_adset_id(self):
        res = mm.delete_adSet(self.token, '-1')
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_ad_creative_valid(self):
        res = mm.create_ad_creative(self.token, 'ad creative name', '49904f214677e640c43989e44cfbe927', self.ad_account,
                                     'oq.com', 'msg')
        body = res.get('body')
        ad_creative_id = body.get('id')
        res = mm.delete_ad_creative(self.token, ad_creative_id)
        status = res.get('status')
        body = res.get('body').get('success')
        self.assertEqual(status, 200)
        self.assertEqual(body, True)

    def test_delete_ad_creative_invalid_token(self):
        res = mm.delete_ad_creative('-1', self.ad_creative)
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_ad_creative_invalid_ad_creative_id(self):
        res = mm.delete_adSet(self.token, '-1')
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_ad(self):
        res = mm.create_ad(self.token, self.ad_account, 'ad name', '120330000357832413', '120330000357828413', 'ACTIVE')
        body = res.get('body')
        ad_id = body.get('id')
        res = mm.delete_ad(self.token, ad_id)
        status = res.get('status')
        body = res.get('body').get('success')
        self.assertEqual(status, 200)
        self.assertEqual(body, True)

    def test_delete_ad_invalid_token(self):
        res = mm.delete_ad('-1', self.ad1)
        status = res.get('status')
        self.assertNotEqual(status, 200)

    def test_delete_ad_invalid_ad_id(self):
        res = mm.delete_ad(self.token, '-1')
        status = res.get('status')
        self.assertNotEqual(status, 200)

    # def test_get_insights(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
