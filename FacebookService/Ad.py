import requests

# ************ Ad MANAGEMENT ************
# *********************************************

# creates a new ad
def create_ad(access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status="PAUSED"):
    if "act_" not in AD_ACCOUNT_ID:
        AD_ACCOUNT_ID = "act_" + AD_ACCOUNT_ID
    url = 'https://graph.facebook.com/v13.0/' + AD_ACCOUNT_ID + '/ads'
    payload = {'name': name,
               'adset_id': adset_id,
               'creative': str({"creative_id": creative_id}),
               "status": status,
               "access_token": access_token
               }
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# get all ads by ad account
def get_all_ads_by_adAcount_id(access_token, ad_account_id):
    url = 'https://graph.facebook.com/v13.0/act_' + ad_account_id + '/ads'
    params = {'fields': 'name',
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}


# get all ads by campaign
def get_all_ads_by_campaign_id(access_token, campaign_id):
    url = 'https://graph.facebook.com/v13.0/' + campaign_id + '/ads'
    params = {'fields': 'name',
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}


# get all ads by adSet id
def get_all_ads_by_adSet_id(access_token, adSet_id):
    url = 'https://graph.facebook.com/v13.0/' + adSet_id + '/ads'
    params = {'fields': 'id,creative,name,status',
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}

# returns: success: bool
def delete_ad(access_token, ad_id):
    url = 'https://graph.facebook.com/v13.0/' + ad_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}