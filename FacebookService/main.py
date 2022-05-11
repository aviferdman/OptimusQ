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

token_details = db.get_GoogleAds_Token('1040281022647-soclnfbgmiujemuojhbopomnkf0o1724.apps.googleusercontent.com',
                                '2838771052')
developer_token = token_details['developer_token']
client_secret = token_details['client_secret']
refresh_token = token_details['refresh_token']

print('hi')
