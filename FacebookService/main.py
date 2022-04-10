import requests
import MarketingManagement

# app_secret = '5e51c4d397a5fa6823d9a1e08f04dc2d'
# app_id = '331878552252931'
# id = 'act_1394987677611796'  # ad account id


# data = {
#     "published": False
# }
# r = requests.post(url, files=files, data=data)
# res = MarketingManagement.add_image('1394987677611796', files["access_token"], 'C:\\Users\\rulid\\Desktop\\airplane.jpg')


# res = MarketingManagement.create_carousel_ad("carousel ad test 1",
#                                              'EAAEt1383MgMBAALZCk5yVm4kxB0immnEfREZA97FH3MZBizRnsb9nXpafKu7n5HqlBUniSA8w2HQ2modIAksLZADoZAhhshcZALLyM80lXOHRU0KWIHZBUo9OxI6yB6lUNChBpN0M3MuxZCSYvHFRzSli7Ur7PY6EPf5FvcovFzBZBRNyov8mMoqTmVY7vDD6qEBj6ZCpZAZCg3SE42JujGYKoSsLq3zqG7VfP7u5jKKBVgHhaz2UcPWj21G',
#                                              '30caa38696f3d8a1cfc9760589f8ce64')


res = MarketingManagement.create_new_campaign('1394987677611796',
                                             'EAAEt1383MgMBAMC7VajQMkfUj57KOtIQpx9H8vbdRvHU9yEKom7amcedmuQrj6aytcv1rQE0zL3bll2jeRfO4rgZB8cIc2gZCv0Q1cSsjnqVhtUjliswyD1dtej1ZBk5h1YSXbcqYh1YSRiN9aYpi1BPEe5rvx6I8zQJOr0NlNm0hLQRjypOn5YQMju2iInyVO5xz6m0L1VXyRvNJGT4veFY9jp5SoZBPMCzIjZAlNc5sHK78XMuh',
                                              'camp 10.4', "PAGE_LIKES", 'PAUSED', "[]")

print('hi')
