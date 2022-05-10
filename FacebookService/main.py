import MarketingManagement as mm
# sandbox details:
# sandbox ad account id: 1107831820072468
# campaign: '{"id":"120330000357827313"}'
# adset: '{"id":"120330000357832413"}'
# img_hash: '49904f214677e640c43989e44cfbe927'
# adCreative: '{"id":"120330000357828413"}'
# ad id for example: '{"id":"120330000357835013"}'
# ad 2 id: {'id': '120330000357977413'}

from DataBaseService.main import dataBaseController

db = dataBaseController
token = db.getAccessTokenByUserId('sandbox_token')

res = mm.get_all_campaigns(token, '1107831820072468')
print('hi')
