import requests
import MarketingManagement

import urllib.request
import base64

# data = {
#     "published": False
# }
# r = requests.post(url, files=files, data=data)
# res = MarketingManagement.add_image('1394987677611796', files["access_token"], 'C:\\Users\\rulid\\Desktop\\airplane.jpg')







# res= MarketingManagement.upload_image_by_url('1394987677611796',
#                                       '',
#                                       'https://blog.hubspot.com/hubfs/marketing-techniques-Jun-30-2020-04-25-34-14-AM.jpg')
# data = res.json()['data']
# res1 = urlopen("https://pixabay.com/get/g6d2311ceb47ef9f90b39b9bb1e5c13f8b1841213644c94cf5e32c2f3b075c316df846fb2889ff1147d427d1faa9fddd9_640.jpg")
# res2 = res1.read()
# res3 = base64.b64encode(res2)
# res2 = base64.b64encode(urlopen("https://pixabay.com/get/g6d2311ceb47ef9f90b39b9bb1e5c13f8b1841213644c94cf5e32c2f3b075c316df846fb2889ff1147d427d1faa9fddd9_640.jpg").read())


# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#
# url = "https://pixabay.com/get/ge5a8307f6020f1bc5c4551006aadc3b8c99d96203660658f24be70a378d77429107845b9dc4180c9e39c8af1f3a2cc74892c5beba7264b097a0ebd6b4403748e_640.png"
# headers={'User-Agent':user_agent,}
#
# request=urllib.request.Request(url,None,headers) #The assembled request
# response = urllib.request.urlopen(request)
# data = response.read() # The data u need

# res = base64.b64encode(data)


# s = base64.urlsafe_b64encode(data).decode()

# s2= str(s)
#
# encoded_string= base64.b64encode(data) # the encode we need!

# encoded_str = str(encoded_string)

res = MarketingManagement.upload_image_by_url('1394987677611796',
                                              'EAAEt1383MgMBAB2FZCHtFgYbnrlJBWlWZCFgfOH7QggFM0nMZCZAuoOwIFoIXPkjZAlMi0Bm0ShHC7uvso6mU5oxLr1fQakgtjWjvhZCpqmcraGzoiKJZBUthhjyAw8v7SqiYllPShI4auW6uZBEPLZBcvZAgc1xCucrqxQqLy8rKgE9Kv2OtwzQk5ZCEoTzuJRYN0gyx7evsYqStqHFD1eiSFZAR8tfa0wYPLx9vO2ZCbz0iHfwSspJE9IgZC',
                                              'https://pixabay.com/get/ge2b26680189f004db205a96101aa57e45807e44f7150e776d9abb969cf16a2152053b0d56bec4c71757c6108666899b16a10007ddde52f8afb0fef3be32c12a9_640.png')

# data = res.json()["images"]["bytes"]["hash"]
print('hi')

