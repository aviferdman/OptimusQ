import requests
import MarketingManagement



# data = {
#     "published": False
# }
# r = requests.post(url, files=files, data=data)
# res = MarketingManagement.add_image('1394987677611796', files["access_token"], 'C:\\Users\\rulid\\Desktop\\airplane.jpg')







res= MarketingManagement.get_all_ads_by_adSet_id('', '23850154047300253')
# data = res.json()['data']
id = res.json()['data']
print('hi')
