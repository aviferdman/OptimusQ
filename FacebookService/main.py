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


db = dataBaseController
token = db.getAccessTokenByUserId('sandbox_token')

adsets = mm.get_all_ads_by_adAcount_id(token, sandbox_ad_account).get('body').get('data')
count = 0
for ad_set in adsets:
    id = ad_set.get('id')
    if id != '120330000357835013' and id != '120330000357977413':
        res = mm.delete_ad(token, id)
        count += 1
print(count)
print('hi')
