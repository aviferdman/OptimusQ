import unittest
from unittest.mock import Mock, MagicMock
from ImageService import main

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.imageService = main
        self.httpRequestMock = MagicMock()

    def test_something_1(self):
        data = {
            "stock": "shutterstock",
            "keywords": ["banana", "apple", "egg", "monkey"],
            "maxImages": [5, 4, 3, 2],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        for keyword in res["images"]:
            self.assertIn(keyword, data["keywords"])
        self.assertLessEqual(len(res["images"]), main.maxValidKeyword)

    def test_something_2(self):
        data = {
            "stock": "shutterstock",
            "keywords": ["apple"],
            "maxImages": [3, 1],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_3(self):
        data = {
            "stock": "shutterstock",
            "keywords": ["banana", "apple"],
            "maxImages": [3],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_4(self):
        data = {
            "stock": "shutterstock",
            "keywords": ["banana", "apple"],
            "maxImages": [3, 1],
            "properties": "wowow"
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_5(self):
        data = {
            "stock": "pixable",
            "keywords": [],
            "maxImages": [],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_6(self):
        data = {
            "stock": "pixable",
            "keywords": ["banana"],
            "maxImages": [5],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        for keyword in res["images"]:
            self.assertIn(keyword, data["keywords"])
        self.assertLessEqual(len(res["images"]), main.maxValidKeyword)

    def test_something_7(self):
        data = {
            "stock": "pixable",
            "keywords": ["banana", "apple"],
            "maxImages": [3],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_8(self):
        data = {
            "stock": "pixable",
            "keywords": ["apple"],
            "maxImages": [3, 1],
            "properties": "nana"
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_9(self):
        data = {
            "stock": "pixable",
            "keywords": ["apple"],
            "maxImages": [3, "banana"],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_10(self):
        data = {
            "stock": "pixable",
            "keywords": ["apple", 3],
            "maxImages": [3, 1],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_something_11(self):
        data = {
            "stock": "shoko",
            "keywords": ["sky"],
            "maxImages": [7],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)


if __name__ == '__main__':
    unittest.main()
