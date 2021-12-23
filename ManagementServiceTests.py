import unittest
from unittest.mock import Mock, MagicMock
from ManagementService.ManagementServiceLibrary import main

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.managementService = main
        self.httpRequestMock = MagicMock()
    
    def test_something_1(self):
        data = {
            "landingPage": "microsoft.com",
            "stock": "shutterstock",
            "keywords": ["banana", "apple", "egg", "monkey"],
            "maxImages": [5, 4, 3, 2],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res = main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        for keyword in res["images"]:
            self.assertIn(keyword, data["keywords"])
        self.assertLessEqual(len(res["images"]), main.maxValidKeyword)



if __name__ == '__main__':
    unittest.main()
