import unittest
from unittest.mock import Mock, MagicMock
from ManagementService.ManagementServiceLibrary import main


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.httpRequestMock = MagicMock()

    def test_happy_shutterstock(self):
        data = {
            "landingPage": "https://www.microsoft.com/en-il/",
            "stock": "shutterstock",
            "imageServiceProperties": {
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)
        self.assertTrue(len(response["images"]) > 0)

    def test_happy_pixable(self):
        data = {
            "landingPage": "https://www.microsoft.com/en-il/",
            "stock": "pixable",
            "imageServiceProperties": {
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)
        self.assertTrue(len(response["images"]) > 0)

    def test_bad_landingpage_shutterstock(self):
        data = {
            "landingPage": "bad",
            "stock": "shutterstock",
            "imageServiceProperties": {
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) == 0)
        self.assertTrue(len(response["images"]) == 0)

    def test_bad_landingpage_pixable(self):
        data = {
            "landingPage": "bad",
            "stock": "pixable",
            "imageServiceProperties": {
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) == 0)
        self.assertTrue(len(response["images"]) == 0)

    def test_bad_stock_pixable(self):
        data = {
            "landingPage": "https://www.microsoft.com/en-il/",
            "stock": "bad",
            "imageServiceProperties": {
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)
        self.assertTrue(len(response["images"]) == 0)

    def test_bad_image_properties_pixable(self):
        data = {
            "landingPage": "https://www.microsoft.com/en-il/",
            "stock": "pixable",
            "imageServiceProperties": {
                "bad": "bad"
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)
        self.assertTrue(len(response["images"]) > 0)

    def test_bad_image_properties_pixable(self):
        data = {
            "landingPage": "https://www.microsoft.com/en-il/",
            "stock": "shutterstock",
            "imageServiceProperties": {
                "bad": "bad"
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)
        self.assertTrue(len(response["images"]) > 0)

    def test_sad_landingpage_pixable(self):
        data = {
            "landingPage": "https://www.ynet.com",
            "stock": "shutterstock",
            "imageServiceProperties": {
                "bad": "bad"
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)

    def test_sad_landingpage_pixable(self):
        data = {
            "landingPage": "https://www.ynet.com",
            "stock": "pixable",
            "imageServiceProperties": {
                "bad": "bad"
            }
        }
        self.httpRequestMock.get_json.return_value = data
        response = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(response), dict)
        self.assertTrue(len(response["keywords"]) > 0)


if __name__ == '__main__':
    unittest.main()
