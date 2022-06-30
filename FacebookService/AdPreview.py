import requests

# ************ Ad Preview ************
# *********************************************

# get an adCreative preview
def get_adCreative_preview(access_token, creative_id, ad_format='DESKTOP_FEED_STANDARD'):
    url = 'https://graph.facebook.com/v13.0/' + creative_id + '/previews'
    params = {'ad_format': ad_format,
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}


# get an ad preview
def get_ad_preview(access_token, ad_id, ad_format='DESKTOP_FEED_STANDARD'):
    url = 'https://graph.facebook.com/v13.0/' + ad_id + '/previews'
    params = {'ad_format': ad_format,
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}