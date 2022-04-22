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


# res = MarketingManagement.create_new_campaign('1394987677611796',
#                                              'EAAEt1383MgMBAMlyYiZCCurOfgUmB0ZBPDjODZCNBQfEgsk2UK68mHsm0gL1JHHUWSjT3BL6vpcw8r0Fnl84VeD9yzxpE9iTOJFxAA9YZCmCxEpXTBKie5iz8y3ZC7CvZCzVZBKDvzph40znwHe6GGN55dMz8FeyphkMA98SEztdnlwCLU4z06DUdc5nTDfuQOpax45pK0TxIp8ZA6MgdQyg',
#                                               'camp 19.4', "PAGE_LIKES", 'PAUSED', "[]")

res= MarketingManagement.get_all_ads_by_adSet_id('EAAEt1383MgMBAIk1MeMDpTQQlJ7UOI7mh8LWCyV0psrckPCcg7uMvFvV2xnLUAhS2IpZBjgSZA3zFpTX3NxFZAaIEaHpNZB6pt3ZA80VXIPBnpdiW3TlLCgMbft4mSZCsH3Mu2JcgguWgwgvmU49JEAQCrrZA2tv5SEL2ZBb3OdBBc4RFm7V154HNfBEu65IA0ViZC28ZCJXwrVOgtTziiFWy7mvFKpJzfDCR8joDBwJDZCEql7cjJdgDB1', '23850154047300253')
# data = res.json()['data']
id = res.json()['data']
print('hi')
