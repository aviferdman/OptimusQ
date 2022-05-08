import unittest
import time

from DataBaseService.main import DataBaseController


class FBDBTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DataBaseController()

    # test campaigns
    def test_add_campaign(self):
        time_in_millis = round(time.time() * 1000)
        self.assertEqual(len(self.db.getCampaign(time_in_millis)), 0)
        self.db.addCampaign(str(time_in_millis), '1107831820072468', 'name1', 'objective', 'ACTIVE')
        self.assertEqual((self.db.getCampaign(time_in_millis))[0][0], str(time_in_millis))

    def test_get_campaign(self):
        self.assertEqual((self.db.getCampaign('120330000357827313'))[0][2], 'camp1')

    def test_get_all_campaigns(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addCampaign(str(time_in_millis), '1107831820072468', 'name1', 'objective', 'ACTIVE')
        self.assertEqual(len(self.db.getAllCampaigns()) > 0, True)

    def test_delete_campaign(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addCampaign(str(time_in_millis), '1107831820072468', 'name1', 'objective', 'ACTIVE')
        self.assertEqual(len(self.db.getCampaign(time_in_millis)) > 0, True)
        self.db.deleteCampaign(time_in_millis)
        self.assertEqual(len(self.db.getCampaign(time_in_millis)) == 0, True)

    # test ad sets
    def test_get_adSet(self):
        self.assertEqual((self.db.getAdSet('120330000357832413'))[0][3], 'name')

    def test_add_adSet(self):
        time_in_millis = round(time.time() * 1000)
        self.assertEqual(len(self.db.getAdSet(time_in_millis)), 0)
        self.db.addAdSet(str(time_in_millis), '1107831820072468', '120330000357827313', 'name1', 1000, 'age_max:65,age_min:18,countries:[US],location_types:[home]')
        self.assertEqual((self.db.getAdSet(time_in_millis))[0][0], str(time_in_millis))

    def test_get_all_adSets(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addAdSet(str(time_in_millis), '1107831820072468', '120330000357827313', 'name1', 1000, 'age_max:65,age_min:18,countries:[US],location_types:[home]')
        self.assertEqual(len(self.db.getAllAdSets()) > 0, True)

    def test_delete_adSet(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addAdSet(str(time_in_millis), '1107831820072468', '120330000357827313', 'name1', 1000, 'age_max:65,age_min:18,countries:[US],location_types:[home]')
        self.assertEqual(len(self.db.getAdSet(time_in_millis)) > 0, True)
        self.db.deleteAdSet(time_in_millis)
        self.assertEqual(len(self.db.getAdSet(time_in_millis)) == 0, True)

    # test images
    def test_add_fb_img(self):
        time_in_millis = round(time.time() * 1000)
        self.assertEqual(len(self.db.getFBImage(time_in_millis)), 0)
        self.db.addFBImage(str(time_in_millis), 'img url')
        self.assertEqual((self.db.getFBImage(time_in_millis))[0][1], 'img url')

    def test_get_fb_img(self):
        self.assertEqual((self.db.getFBImage('1652016508800'))[0][0], '1652016508800')

    def test_get_all_fb_images(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addFBImage(str(time_in_millis), 'img url')
        self.assertEqual(len(self.db.getAllFBImages()) > 0, True)

    def test_delete_fb_image(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addFBImage(str(time_in_millis), 'img url')
        self.assertEqual(len(self.db.getFBImage(time_in_millis)) > 0, True)
        self.db.deleteFBImage(time_in_millis)
        self.assertEqual(len(self.db.getFBImage(time_in_millis)) == 0, True)

    # test ad creatives
    def test_add_fb_AdCreative(self):
        time_in_millis = round(time.time() * 1000)
        self.assertEqual(len(self.db.getFBAdCreative(time_in_millis)), 0)
        self.db.addFBAdCreative(str(time_in_millis), 'name',
                    'title',
                    'body',
                    '1652016508800')
        self.assertEqual((self.db.getFBAdCreative(time_in_millis))[0][1], 'name')

    def test_get_fb_AdCreative(self):
        self.assertEqual((self.db.getFBAdCreative('120330000357828413'))[0][2], 'title')

    def test_get_all_fb_AdCreatives(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addFBAdCreative(str(time_in_millis), 'name',
                    'title',
                    'body',
                    '1652016508800')
        self.assertEqual(len(self.db.getAllFBAdCreatives()) > 0, True)

    def test_delete_fb_AdCreative(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addFBAdCreative(str(time_in_millis), 'name',
                    'title',
                    'body',
                    '1652016508800')
        self.assertEqual(len(self.db.getFBAdCreative(time_in_millis)) > 0, True)
        self.db.deleteFBAdCreative(time_in_millis)
        self.assertEqual(len(self.db.getFBAdCreative(time_in_millis)) == 0, True)

    # test ads
    def test_add_fb_Ad(self):
        time_in_millis = round(time.time() * 1000)
        self.assertEqual(len(self.db.getFBAd(time_in_millis)), 0)
        self.db.addFBAd(str(time_in_millis), '120330000357832413', 'ad name', '120330000357828413', 'PAUSED')
        self.assertEqual((self.db.getFBAd(time_in_millis))[0][2], 'ad name')

    def test_get_fb_Ad(self):
        self.assertEqual((self.db.getFBAd('120330000357835013'))[0][2], 'name')

    def test_get_all_fb_Ads(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addFBAd(str(time_in_millis), '120330000357832413', 'ad name', '120330000357828413', 'PAUSED')
        self.assertEqual(len(self.db.getAllFBAds()) > 0, True)

    def test_delete_fb_Ad(self):
        time_in_millis = round(time.time() * 1000)
        self.db.addFBAd(str(time_in_millis), '120330000357832413', 'ad name', '120330000357828413', 'PAUSED')
        self.assertEqual(len(self.db.getFBAd(time_in_millis)) > 0, True)
        self.db.deleteFBAd(time_in_millis)
        self.assertEqual(len(self.db.getFBAd(time_in_millis)) == 0, True)


if __name__ == '__main__':
    unittest.main()
