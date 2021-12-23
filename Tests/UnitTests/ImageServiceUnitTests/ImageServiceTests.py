import unittest
from unittest.mock import Mock, MagicMock
from ImageService import main
class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.imageService = main
        self.httpRequestMock = MagicMock()

    def test_valid_shutterstock(self):
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

    def test_invalidLength_1(self):
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

    def test_invalidLength_2(self):
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

    def test_invalidProperties(self):
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

    def test_emptyData(self):
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

    def test_valid_pixable(self):
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

    def test_lessThanMaxValidKeywords(self):
        data = {
            "stock": "pixable",
            "keywords": ["banana", "lemon", "pineapple", "monkey", "dog", "cat"],
            "maxImages": [5],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertLessEqual(len(res["images"]), main.maxValidKeyword)

    def test_invalidLength_3(self):
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

    def test_invalidLength_4(self):
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

    def test_invalidLength_5(self):
        data = {
            "stock": "pixable",
            "keywords": ["apple"],
            "maxImages": [3, 7],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_invalidMaxImagesValue(self):
        data = {
            "stock": "pixable",
            "keywords": ["apple", "banana"],
            "maxImages": [3, "banana"],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        self.assertEqual(type(res), dict)
        self.assertEqual(bool(res["images"]), False)

    def test_keywordValue_1(self):
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

    def test_invalidStock(self):
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

    def test_lessThanEachMaxLength_1(self):
        data = {
            "stock": "pixable",
            "keywords": ["banana", "lemon", "pineapple", "monkey", "dog", "cat"],
            "maxImages": [5, 1, 0, 37, 2, 3],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        for keyword in res["images"]:
            x = len(res["images"][keyword])
            y = data["maxImages"][data["keywords"].index(keyword)]
            self.assertLessEqual(x, y)

    def test_lessThanEachMaxLength_2(self):
        data = {
            "stock": "shutterstock",
            "keywords": ["banana", "lemon", "pineapple", "monkey", "dog", "cat"],
            "maxImages": [5, 1, 0, 37, 2, 3],
            "properties": {}
        }
        self.httpRequestMock.get_json.return_value = data
        res =main.main_trigger(self.httpRequestMock)
        for keyword in res["images"]:
            x = len(res["images"][keyword])
            y = data["maxImages"][data["keywords"].index(keyword)]
            self.assertLessEqual(x, y)


if __name__ == '__main__':
    unittest.main()
