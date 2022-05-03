import requests
import urllib.request
import base64

# This interface allows the user to create and manage all the marketing fields,
# using Facebook APIs.

business_id = 775308013448374  # initial business id


# updated business_id
def set_business_id(new_id):
    business_id = new_id


# generate a new APP_ACCESS_TOKEN
def generate_new_app_access_token(app_id, app_secret):
    url = 'https://graph.facebook.com/oauth/access_token'
    payload = {'client_id': '' + app_id,
               'client_secret': '' + app_secret,
               "grant_type": "client_credentials"}
    return requests.post(url, data=payload, headers={})


# create a new ad account
# for free business account, there's a limit for only 1 ad account!
def create_ad_account(business_id, account_name, access_token, currency, timezone_id,
                      end_advertiser='NONE', media_agency='NONE', partner='NONE'):
    url = 'https://graph.facebook.com/v13.0/' + business_id + '/adaccount'
    payload = {'name': account_name,
               'currency': currency,
               "timezone_id": timezone_id,
               'end_advertiser': end_advertiser,
               'media_agency': media_agency,
               'partner': partner,
               'access_token': access_token}
    return requests.post(url, data=payload, headers={})


# get ad account by id
def get_ad_account_by_id(ad_account_id, access_token):
    fields = 'fields=account_id,name,account_status,amount_spent,currency,owner,timezone_name,campaigns{id,name}'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/act_' + ad_account_id + '/?' +
                        fields, params)


# returns all ad accounts belongs to business_id
def get_all_ad_accounts_in_business(access_token):
    fields = 'fields=amount_spent,business,name,account_id'
    params = {'access_token': access_token}
    return requests.get('https://graph.facebook.com/v13.0/' + str(business_id) + '/owned_ad_accounts?' + fields, params)


# creates a new campaign.
# all params are string. special_ad_categories in the form: "[]"
# returns: new campaign's id
def create_new_campaign(ad_account_id, access_token, campaign_name, objective="LINK_CLICKS",
                        status="PAUSED", special_ad_categories="[]"):
    url = 'https://graph.facebook.com/v13.0/act_' + ad_account_id + '/campaigns'
    payload = {'name': campaign_name,
               'objective': objective,
               "status": status,
               'special_ad_categories': special_ad_categories,
               'access_token': access_token}
    return requests.post(url, data=payload, headers={})


# returns a campaign by id
def get_campaign_by_id(access_token, campaign_id):
    fields = 'fields=adsets{id,name,created_time,bid_info,budget_remaining,daily_budget,effective_status,end_time,status,targeting,ads{id,name,adcreatives{id,name}}}'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/' + campaign_id + '/?' +
                        fields, params)


# returns all campaign belongs to AD_ACCOUNT_ID
def get_all_campaigns(ad_account_id, access_token):
    params = {
        'access_token': access_token
    }
    return requests.get(
        'https://graph.facebook.com/v13.0/act_' + ad_account_id + '?fields=campaigns{id,name,budget_remaining,daily_budget}',
        params)


# creates a new ad set
def create_new_ad_set(AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, daily_budget="1000",
                      optimization_goal='REACH',
                      billing_event='IMPRESSIONS', bid_amount="2",
                      targeting={"geo_locations": {"countries": ["US"]}},
                      start_time='2020-10-06T04:45:17+0000', status='PAUSED'):
    url = 'https://graph.facebook.com/v13.0/act_' + AD_ACCOUNT_ID + '/adsets'
    payload = {'name': ad_set_name,
               'optimization_goal': optimization_goal,
               "billing_event": billing_event,
               "bid_amount": bid_amount,
               "daily_budget": daily_budget,
               "campaign_id": campaign_id,
               "targeting": str(targeting),
               "start_time": start_time,
               "status": status,
               "access_token": access_token
               }
    return requests.post(url, data=payload, headers={})


# returns all ad sets belongs to AD_ACCOUNT_ID
def get_all_ad_sets_by_ad_account(access_token, ad_account_id):
    fields = 'fields=daily_budget,name,targeting'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/act_' + ad_account_id + '/adsets?' + fields, params)


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_path(AD_ACCOUNT_ID, access_token, image_path):
    image_file = open(image_path, "rb")
    url = 'https://graph.facebook.com/v13.0/act_' + AD_ACCOUNT_ID + '/adimages'
    file_obj = {'filename': image_file}
    payload = {"access_token": access_token}
    return requests.post(url, data=payload, files=file_obj)


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_url(AD_ACCOUNT_ID, access_token, image_url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(image_url, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()  # The data we need
    image_file = base64.b64encode(data).decode()
    url = 'https://graph.facebook.com/v13.0/act_' + AD_ACCOUNT_ID + '/adimages'
    file_obj = {'bytes': image_file}
    payload = {"access_token": access_token}
    return requests.post(url, data=payload, params=file_obj)


# creates a new ad creative
# todo: returns error: "Ads creative post was created by an app that is in development mode. It must be in public to create this ad"
# todo: make this function generic
def create_ad_creative(name, access_token, image_hash, ad_account_id, link, message, page_id='107414948611212'):
    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "image_hash": image_hash,
            "link": link,
            "message": message
        }
    }
    url = 'https://graph.facebook.com/v13.0/act_' + ad_account_id + '/adcreatives'
    payload = {'name': name,
               'object_story_spec': str(object_story_spec),
               "access_token": access_token
               }
    return requests.post(url, data=payload, headers={})


# creates an ad of type "carousel"
# todo: make this function generic
def create_carousel_ad(name, access_token, image_hash, link, description, page_id='107414948611212'):
    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "child_attachments": [
                {
                    "description": description,
                    "image_hash": image_hash,
                    "link": link,
                    "name": "Product 1",
                    # "video_id": "<VIDEO_ID>"
                },
                {
                    "description": "$1.99",
                    "image_hash": image_hash,
                    "link": "https://www.ynet.co.il/",
                    "name": "Product 2",
                    # "video_id": "<VIDEO_ID>"
                }
            ],

            "link": "https://facebook.com/109098168429622",
        }
    }
    url = 'https://graph.facebook.com/v13.0/act_1394987677611796/adcreatives'
    payload = {'name': name,
               'object_story_spec': str(object_story_spec),
               "access_token": access_token
               }
    return requests.post(url, data=payload, headers={})


# creates a new ad
def create_ad(access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status="PAUSED"):
    url = 'https://graph.facebook.com/v13.0/act_' + AD_ACCOUNT_ID + '/ads'
    payload = {'name': name,
               'adset_id': adset_id,
               'creative': str({"creative_id": creative_id}),
               "status": status,
               "access_token": access_token
               }
    return requests.post(url, data=payload, headers={})


# get all ads by ad account
def get_all_ads_by_adAcount_id(access_token, ad_account_id):
    url = 'https://graph.facebook.com/v13.0/act_' + ad_account_id + '/ads'
    params = {'fields': 'name',
              "access_token": access_token
              }
    return requests.get(url, params)


# get all ads by campaign
def get_all_ads_by_campaign_id(access_token, campaign_id):
    url = 'https://graph.facebook.com/v13.0/' + campaign_id + '/ads'
    params = {'fields': 'name',
              "access_token": access_token
              }
    return requests.get(url, params)


# get all ads by adSet id
def get_all_ads_by_adSet_id(access_token, adSet_id):
    url = 'https://graph.facebook.com/v13.0/' + adSet_id + '/ads'
    params = {'fields': 'name',
              "access_token": access_token
              }
    return requests.get(url, params)


# You cannot remove ad accounts from your business if you're OWNER and if the accounts are CONFIRMED.
# If you have a PENDING access request or you have AGENCY access to the ad account, you can make this DELETE call
def delete_ad_account(access_token, business_id, ad_account_id):
    url = 'https://graph.facebook.com/v13.0/' + business_id + '/ad_accounts'
    payload = {'adaccount_id': ad_account_id,
               "access_token": access_token
               }
    return requests.delete(url, data=payload, headers={})


# returns: success: bool
def delete_campaign(access_token, campaign_id):
    url = 'https://graph.facebook.com/v13.0/' + campaign_id
    payload = {"access_token": access_token}
    return requests.delete(url, data=payload, headers={})


# returns: success: bool
def delete_adSet(access_token, adSet_id):
    url = 'https://graph.facebook.com/v13.0/' + adSet_id
    payload = {"access_token": access_token}
    return requests.delete(url, data=payload, headers={})


# returns: success: bool
def delete_ad_creative(access_token, ad_creative_id):
    url = 'https://graph.facebook.com/v13.0/' + ad_creative_id
    payload = {"access_token": access_token}
    return requests.delete(url, data=payload, headers={})


# returns: success: bool
def delete_ad(access_token, ad_id):
    url = 'https://graph.facebook.com/v13.0/' + ad_id
    payload = {"access_token": access_token}
    return requests.delete(url, data=payload, headers={})


# get statistics by campaign id
# todo: implement
def get_campaign_statistics(campaign_id, access_token):
    pass
