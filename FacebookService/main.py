import json

import MarketingManagement as mm
from DataBaseService.main import dataBaseController


# sandbox details:
# sandbox ad account id: 1107831820072468
sandbox_ad_account = '1107831820072468'
# campaign: '{"id":"120330000357827313"}'
campaign = '120330000357827313'
# adset: '{"id":"120330000357832413"}'
adset = '120330000357832413'
# img_hash: '49904f214677e640c43989e44cfbe927'
img_hash = '49904f214677e640c43989e44cfbe927'
# ad_creative: '{"id":"120330000357828413"}'
ad_creative = '120330000357828413'
# ad id for example: '{"id":"120330000357835013"}'
ad1 = '120330000357835013'
# ad 2 id: {'id': '120330000357977413'}
ad2 = '120330000357977413'
interest1 = '6003539884903'
interest2 = '6003107902433'
behavior1 = '6002714895372'
behavior2 = '6004385868372'


db = dataBaseController
token = db.getAccessTokenByUserId('sandbox_token')
admin_token = db.getAccessTokenByUserId('admin_token')

# targeting = {"age_min": 12, "age_max": 40, "geo_locations": {"countries": ["US", "IL"]}}
# res1 = mm.create_new_ad_set(token, sandbox_ad_account, 'adSet name 5', campaign)
# res = mm.upload_image_by_url(token, "1107831820072468", "https://en.spitogatos.gr/frontend/images/homepage/sg_04.jpg")
# res = mm.upload_image_by_path(token, sandbox_ad_account, 'C:\\Users\\rulid\\Desktop\\graduation-2613183_1920.jpg')


print('hi')
