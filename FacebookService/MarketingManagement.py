import time

import requests
import urllib.request
import base64
from DataBaseService.main import dataBaseController
import io

# This interface allows the user to create and manage all the marketing fields,
# using Facebook APIs.

business_id = 775308013448374  # OQ business id
OQ_app_id = 331878552252931
db = dataBaseController

behaviors_from_db = db.getAllFBTargetingBehaviors()

# maps campaign objective to its possible optimization goals
map_objective_to_possible_opt_goal = {
    "APP_INSTALLS": "APP_INSTALLS",
    "BRAND_AWARENESS": "AD_RECALL_LIFT,REACH",
    "CONVERSIONS": "OFFSITE_CONVERSIONS,IMPRESSIONS,LINK_CLICKS,POST_ENGAGEMENT,REACH,VALUE,LANDING_PAGE_VIEWS,CONVERSATIONS",
    "EVENT_RESPONSES": "EVENT_RESPONSES,IMPRESSIONS,REACH",
    "LEAD_GENERATION": "LEAD_GENERATION,QUALITY_LEAD,LINK_CLICKS,QUALITY_CALL",
    "LINK_CLICKS": "LINK_CLICKS,IMPRESSIONS,POST_ENGAGEMENT,REACH,LANDING_PAGE_VIEWS",
    "MESSAGES": "CONVERSATIONS,IMPRESSIONS,POST_ENGAGEMENT,LEAD_GENERATION,LINK_CLICKS",
    "PAGE_LIKES": "PAGE_LIKES,IMPRESSIONS,POST_ENGAGEMENT,REACH",
    "POST_ENGAGEMENT": "POST_ENGAGEMENT,IMPRESSIONS,REACH,LINK_CLICKS",
    "PRODUCT_CATALOG_SALES": "OFFSITE_CONVERSIONS,LINK_CLICKS,IMPRESSIONS,POST_ENGAGEMENT,REACH,CONVERSATIONS,VALUE",
    "REACH": "REACH,IMPRESSIONS",
    "VIDEO_VIEWS": "THRUPLAY"
}

# maps optimization goal to possible billing events
map_opt_goal_to_possible_billing_events = {
    "APP_INSTALLS": "IMPRESSIONS",
    "AD_RECALL_LIFT": "IMPRESSIONS",
    "ENGAGED_USERS": "IMPRESSIONS",
    "EVENT_RESPONSES": "IMPRESSIONS",
    "IMPRESSIONS": "IMPRESSIONS",
    "LEAD_GENERATION": "IMPRESSIONS",
    "LINK_CLICKS": "LINK_CLICKS,IMPRESSIONS",
    "OFFSITE_CONVERSIONS": "IMPRESSIONS",
    "PAGE_LIKES": "IMPRESSIONS",
    "POST_ENGAGEMENT": "IMPRESSIONS",
    "REACH": "IMPRESSIONS",
    "REPLIES": "IMPRESSIONS",
    "SOCIAL_IMPRESSIONS": "IMPRESSIONS",
    "THRUPLAY": "IMPRESSIONS,THRUPLAY",
    "VALUE": "IMPRESSIONS",
    "LANDING_PAGE_VIEWS": "IMPRESSIONS"
}

all_possible_campaign_objectives = "APP_INSTALLS,BRAND_AWARENESS,CONVERSIONS,EVENT_RESPONSES,LEAD_GENERATION," \
                                   "LINK_CLICKS,MESSAGES,PAGE_LIKES,POST_ENGAGEMENT,PRODUCT_CATALOG_SALES,REACH," \
                                   "VIDEO_VIEWS"
all_possible_campaign_objectives_lst = all_possible_campaign_objectives.split(",")

all_possible_opt_goals = set()
for objective in all_possible_campaign_objectives_lst:
    for opt_goal in map_objective_to_possible_opt_goal[objective].split(","):
        all_possible_opt_goals.add(opt_goal)


# get all possible campaign objectives
def get_all_possible_campaign_objectives():
    return {"status": 200, "body": all_possible_campaign_objectives}


# get all optimization goals for objective
def get_all_optimization_goals_for_objective(objective):
    return {"status": 200, "body": map_objective_to_possible_opt_goal[objective]}


# get all possible billing events for opt goal
def get_all_possible_billing_events_for_opt_goal(opt_goal):
    return {"status": 200, "body": map_opt_goal_to_possible_billing_events[opt_goal]}


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
def create_ad_account(access_token, business_id, account_name, currency, timezone_id,
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
def get_ad_account_by_id(access_token, ad_account_id):
    fields = 'fields=account_id,name,account_status,amount_spent,currency,owner,timezone_name,campaigns{id,name}'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/act_' + ad_account_id + '/?' +
                        fields, params)


# returns all ad accounts belong to business_id
def get_all_ad_accounts_in_business(access_token, business_id):
    fields = 'fields=owned_ad_accounts{name,account_id}'
    params = {'access_token': access_token}
    res = requests.get('https://graph.facebook.com/v13.0/' + business_id + '?' + fields, params)
    return res


# creates a new campaign.
# all params are string. special_ad_categories in the form: "[]"
# returns: new campaign's id
def create_new_campaign(access_token, ad_account_id, campaign_name, objective="LINK_CLICKS",
                        status="PAUSED", special_ad_categories="[]"):
    if "act_" not in ad_account_id:
        ad_account_id = "act_" + ad_account_id
    url = 'https://graph.facebook.com/v13.0/' + ad_account_id + '/campaigns'
    payload = {'name': campaign_name,
               'objective': objective,
               "status": status,
               'special_ad_categories': special_ad_categories,
               'access_token': access_token}
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns a campaign by id
def get_campaign_by_id(access_token, campaign_id):
    fields = 'fields=id,name,budget_remaining,daily_budget,objective'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + campaign_id + '/?' +
                       fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all campaign belongs to AD_ACCOUNT_ID
def get_all_campaigns(access_token, ad_account_id):
    fields = 'fields=campaigns{budget_remaining,can_create_brand_lift_study,configured_status,created_time,name,objective,special_ad_categories,start_time,status,updated_time}'
    params = {
        'access_token': access_token
    }
    res = requests.get(
        'https://graph.facebook.com/v13.0/act_' + ad_account_id + '?' + fields, params)
    if res.status_code != 200:
        return {"status": 400, "body": res.json()}
    myRes = {"status": res.status_code, "body": {"data": []}}
    if (res.json() is not None) and (res.json().get('campaigns') is not None) and (
            res.json().get('campaigns').get('data') is not None):
        myRes["body"]["data"] = res.json().get('campaigns').get('data')
    if (res.json() is not None) and (res.json().get('campaigns') is not None) and (
            res.json().get('campaigns').get('paging') is not None):
        myRes["body"]["paging"] = res.json().get('campaigns').get('paging')
    return myRes


# creates a new ad set
def create_new_ad_set(access_token, AD_ACCOUNT_ID, ad_set_name, campaign_id, daily_budget="1000",
                      optimization_goal='REACH',
                      billing_event='IMPRESSIONS', bid_amount="1500",
                      start_time='1633851746', status='PAUSED',
                      targeting_min_age='NONE', targeting_max_age='NONE', targeting_countries=["IL"], end_time='NONE',
                      targeting_gender="NONE", targeting_relationship_statuses="NONE",
                      targeting_interests=[], targeting_behaviors=[], promoted_object=None):
    if "act_" not in AD_ACCOUNT_ID:
        AD_ACCOUNT_ID = "act_" + AD_ACCOUNT_ID
    url = 'https://graph.facebook.com/v13.0/' + AD_ACCOUNT_ID + '/adsets'
    targeting = {}
    if targeting_min_age != 'NONE':
        targeting["age_min"] = targeting_min_age
    if targeting_max_age != 'NONE':
        targeting["age_max"] = targeting_max_age
    targeting["geo_locations"] = {"countries": targeting_countries}
    if targeting_gender != "NONE":
        tmp_lst = list()
        tmp_lst.append(targeting_gender)
        targeting["genders"] = tmp_lst
    if targeting_relationship_statuses != "NONE":
        targeting["relationship_statuses"] = targeting_relationship_statuses
    if len(targeting_interests) > 0:
        targeting["interests"] = targeting_interests
    if len(targeting_behaviors) > 0:
        targeting["behaviors"] = targeting_behaviors

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
    if promoted_object is not None:
        payload["promoted_object"] = str(promoted_object)

    if end_time != 'NONE':
        payload["end_time"] = end_time
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns all ad sets belongs to AD_ACCOUNT_ID
def get_all_ad_sets_by_ad_account(access_token, ad_account_id, with_status="['ACTIVE', 'PAUSED']"):
    fields = 'fields=daily_budget,name,targeting,created_time,billing_event,start_time,end_time,optimization_goal,status,updated_time'
    params = {
        'access_token': access_token
    }
    if with_status != "['ACTIVE', 'PAUSED']":
        params['effective_status'] = with_status
    res = requests.get('https://graph.facebook.com/v13.0/act_' + ad_account_id + '/adsets?' + fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all ad sets belongs to campaign with campaign_id
def get_all_ad_sets_by_campaign(access_token, campaign_id):
    fields = 'fields=daily_budget,name,targeting,created_time,billing_event,start_time,end_time,optimization_goal,status,updated_time,campaign_id,promoted_object,bid_amount'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + campaign_id + '/adsets?' + fields, params)
    if res.status_code != 200:
        return {"status": res.status_code, "body": res.json()}
    myRes = {"status": res.status_code, "body": {"data": []}}
    if res.json().get("paging", None) is not None:
        myRes["body"]["paging"] = res.json().get("paging")
    res_list = list()
    if (res.json() is not None) and (res.json().get('data') is not None):
        for adset in res.json().get('data'):
            if adset.get("targeting", None) is None:
                res_list.append(adset)
                continue
            adset["targeting_min_age"] = adset.get("targeting").get("age_min", None)
            adset["targeting_max_age"] = adset.get("targeting").get("age_max", None)
            targeting_countries_str = ''
            if (adset.get("targeting").get("geo_locations", None) is not None) and (
                    adset.get("targeting").get("geo_locations").get("countries") is not None):
                for country in adset.get("targeting").get("geo_locations").get("countries"):
                    targeting_countries_str += country + ','
            if len(targeting_countries_str) == 0:
                targeting_countries_str = None
            adset["targeting_countries"] = targeting_countries_str
            adset["targeting_interests"] = adset.get("targeting").get("interests", None)
            adset["targeting_behaviors"] = adset.get("targeting").get("behaviors", None)
            if adset.get("targeting").get("genders", None) is not None:
                if len(adset.get("targeting").get("genders")) == 0:
                    adset["targeting_gender"] = None
                else:
                    if (1 in adset.get("targeting").get("genders")) or ('1' in adset.get("targeting").get("genders")):
                        adset["targeting_gender"] = 1
                    else:
                        adset["targeting_gender"] = 2

            targeting_relationship_statuses_str = ''
            if adset.get("targeting").get("relationship_statuses", None) is not None:
                for status in adset.get("targeting").get("relationship_statuses"):
                    targeting_relationship_statuses_str += str(status) + ','
            if len(targeting_relationship_statuses_str) == 0:
                targeting_relationship_statuses_str = None
            adset["targeting_relationship_statuses"] = targeting_relationship_statuses_str
            adset.pop('targeting', None)  # delete targeting for formatting the json
            res_list.append(adset)
    myRes["body"]["data"] = res_list
    return myRes


# returns all ad creatives belongs to ad account
def get_all_ad_creatives(access_token, ad_account):
    fields = 'fields=id,name,title,body,image_hash'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/act_' + ad_account + '/adcreatives?' + fields, params)
    return {"status": res.status_code, "body": res.json()}


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_path(access_token, AD_ACCOUNT_ID, image_path):
    access_token = access_token
    image_file = open(image_path, "rb")
    url = 'https://graph.facebook.com/v13.0/act_' + AD_ACCOUNT_ID + '/adimages'
    file_obj = {'filename': image_file}
    payload = {"access_token": access_token}
    return requests.post(url, data=payload, files=file_obj)


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_url(access_token, AD_ACCOUNT_ID, image_url):
    if "act_" not in AD_ACCOUNT_ID:
        AD_ACCOUNT_ID = "act_" + AD_ACCOUNT_ID
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    try:
        # request = urllib.request.Request(image_url, None, headers)  # The assembled request
        # response = urllib.request.urlopen(request)
        # data = response.read()  # The data we need
        # image_file = base64.b64encode(data).decode()
        url = 'https://graph.facebook.com/v13.0/' + AD_ACCOUNT_ID + '/adimages'

        urllib.request.urlretrieve(image_url, "local-img.jpg")
        image_file = open("local-img.jpg", "rb")

        file_obj = {'filename': image_file}
        payload = {"access_token": access_token}
        res = requests.post(url, data=payload, files=file_obj)
        if res.status_code == 200:
            img_hash = res.json().get('images').get('local-img.jpg').get('hash')
            return {"status": res.status_code, "body": {"hash": img_hash}}
        return {"status": res.status_code, "body": res.json()}
    except Exception as e:
        return {"status": 400, "body": str(e)}


# returns a A permanent URL of the image
def get_permanent_url_for_image_by_hash(access_token, ad_account, hash):
    fields = 'fields=permalink_url'
    params = {
        'hashes': str([hash]),
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/act_' + ad_account + '/adimages?' +
                       fields, params)
    return {"status": res.status_code, "body": res.json()}


# creates a new ad creative
def create_ad_creative(access_token, name, image_hash, ad_account_id, link, message, page_id='107414948611212'):
    if "act_" not in ad_account_id:
        ad_account_id = "act_" + ad_account_id
    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "image_hash": image_hash,
            "link": link,
            "message": message
        }
    }
    url = 'https://graph.facebook.com/v13.0/' + ad_account_id + '/adcreatives'
    payload = {'name': name,
               'object_story_spec': str(object_story_spec),
               "access_token": access_token
               }
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# creates an ad of type "carousel"
# todo: make this function generic
def create_carousel_ad(access_token, name, image_hash, link, description, page_id='107414948611212'):
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

            "link": "https://facebook.com/" + page_id,
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


# You cannot remove ad accounts from your business if you're OWNER and if the accounts are CONFIRMED.
# If you have a PENDING access request or you have AGENCY access to the ad account, you can make this DELETE call
def delete_ad_account(access_token, business_id, ad_account_id):
    url = 'https://graph.facebook.com/v13.0/' + business_id + '/ad_accounts'
    payload = {'adaccount_id': ad_account_id,
               "access_token": access_token
               }
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns: success: bool
def delete_campaign(access_token, campaign_id):
    url = 'https://graph.facebook.com/v13.0/' + campaign_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns: success: bool
def delete_adSet(access_token, adSet_id):
    url = 'https://graph.facebook.com/v13.0/' + adSet_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns: success: bool
def delete_ad_creative(access_token, ad_creative_id):
    url = 'https://graph.facebook.com/v13.0/' + ad_creative_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns: success: bool
def delete_ad(access_token, ad_id):
    url = 'https://graph.facebook.com/v13.0/' + ad_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# get insights for ad account/campaign/ad set/ ad
def get_insights(access_token, marketing_object_id, date_preset='maximum'):
    url = 'https://graph.facebook.com/v13.0/' + marketing_object_id + '/insights'
    params = {'fields': 'impressions,clicks,cpc,ctr,frequency,objective,optimization_goal,quality_ranking,spend',
              'date_preset': date_preset,
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}


# ********** targeting ***********

# search possible interests for ad targeting
def search_for_possible_interests(access_token, q=''):
    url = 'https://graph.facebook.com/v13.0/search'
    params = {'type': 'adinterest',
              'q': q,
              "access_token": access_token
              }

    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}


# get all possible behaviors for ad targeting
def get_all_possible_behaviors(access_token):
    url = 'https://graph.facebook.com/v13.0/search'
    params = {'type': 'adTargetingCategory',
              'class': 'behaviors',
              "access_token": access_token
              }

    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}


# behaviors table in DB must be empty before running this function
def load_all_behaviors_to_db(access_token):
    res = get_all_possible_behaviors(access_token)
    if res.get('status') != 200:
        return
    for behavior in res.get("body").get("data"):
        try:
            id = behavior.get("id")
            name = behavior.get("name")
            path = behavior.get("path")
            paths = ""
            for p in path:
                paths += p + ","
            desc = behavior.get("description")
            audience_size_lower_bound = str(behavior.get("audience_size_lower_bound"))
            audience_size_upper_bound = str(behavior.get("audience_size_upper_bound"))
            db.addFBTargetingBehavior(id, name, audience_size_lower_bound, audience_size_upper_bound, paths, desc)
        except Exception as e:
            print(str(e))


# updates targeting_behaviors DB once a week
def update_targeting_behaviors_once_a_week(access_token):
    while True:
        try:
            time.sleep(604800)
            res = get_all_possible_behaviors(access_token)
            if res.get('status') != 200:
                return

            behaviors_in_db = db.getAllFBTargetingBehaviors()
            behaviors_in_db_ids = list()
            for b in behaviors_in_db:
                behaviors_in_db_ids.append(b[0])
            for behavior in res.get("body").get("data"):
                if behavior.get("id") not in behaviors_in_db_ids:
                    db.addFBTargetingBehavior(behavior.get("id"), behavior.get("name"),
                                              behavior.get("audience_size_lower_bound"),
                                              behavior.get("audience_size_upper_bound"), behavior.get("path"),
                                              behavior.get("description"))

        except Exception as e:
            print(str(e))


# search for behaviors in DB
def search_for_behaviors_in_db(to_search):
    to_search = to_search.lower()
    res = list()
    for b in behaviors_from_db:
        b_str = "" + b[1] + b[4] + b[5]
        b_str = b_str.lower()
        if to_search in b_str:
            res.append({"id": b[0], "name": b[1], "audience_size_lower_bound": b[2],
                        "audience_size_upper_bound": b[3], "path": b[4], "description": b[5]})
            # res.append(tuple(b))

    return res


# ************ BUSINESS MANAGEMENT ************
# *********************************************
def get_all_client_BMs_by_oq_user_id(oq_user_id):
    res_BMs = list()
    try:
        for BM_record in db.getFB_CLIENT_BM_IDS_BY_OQ_USER_ID(oq_user_id):
            res_BMs.append(BM_record[1])
        return {"status": 200, "body": {"data": res_BMs}}
    except Exception as e:
        return {"status": 400, "body": str(e)}


def get_all_client_ad_accounts_by_BM_id(BM_id):
    ad_accounts_ids = list()
    try:
        for record in db.getFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(BM_id):
            ad_accounts_ids.append(record[1])
        return {"status": 200, "body": {"data": ad_accounts_ids}}
    except Exception as e:
        return {"status": 400, "body": str(e)}


def get_all_client_pages_by_BM_id(BM_id):
    pages_ids = list()
    try:
        for record in db.getFB_CLIENT_PAGES_BY_BM_ID(BM_id):
            pages_ids.append(record[1])
        return {"status": 200, "body": {"data": pages_ids}}
    except Exception as e:
        return {"status": 400, "body": str(e)}


# get token for client by oq user id
def get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id):
    try:
        return db.getFB_CLIENT_TOKEN_BY_OQ_USER_ID_AND_BM_ID(oq_user_id, BM_id)[0][4]
    except Exception as e:
        return -1


# returns all businesses by user id: id and name
def get_all_businesses_by_user_id(access_token, user_id):
    fields = 'fields=businesses{id,name}'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v14.0/' + user_id + '?' + fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all business asset groups
def get_all_business_asset_groups(access_token, business_id):
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + business_id + '/business_asset_groups', params)
    return {"status": res.status_code, "body": res.json()}


# returns all ASSETS_IDS for a business, for use in function create_on_behalf_of_relationship
def get_all_business_assets(access_token, business_id):
    fields = 'fields=owned_ad_accounts{name},owned_pages{name}'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + business_id + '?' + fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all pixels ids for business
def get_all_business_pixels(access_token, business_id):
    fields = 'fields=owned_pixels{id,name}'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/' + business_id + '?' + fields, params)


# returns all pixels for ad account
def get_all_ad_account_pixels(access_token, ad_account_id):
    if "act_" not in ad_account_id:
        ad_account_id = "act_" + ad_account_id
    fields = 'fields=adspixels{id,name}'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + ad_account_id + '?' + fields, params)
    if (res.json() is not None) and (res.json().get('adspixels') is not None) and (
            res.json().get('adspixels').get('data') is not None):
        return {"status": res.status_code, "body": {"data": res.json().get('adspixels').get('data')}}
    return {"status": res.status_code, "body": {"data": []}}


# Create the On Behalf Of relationship between the partner and client's Business Manager.
# access token must be the user's and received by FB login - and not the app token.
# API tutorial for this function:
# https://developers.facebook.com/docs/marketing-api/business-manager/guides/on-behalf-of
# ASSETS_IDS is a list, containing assets ids for assigning from client BM to partner BM
def create_on_behalf_of_relationship(client_admin_access_token, client_user_id, oq_user_id):
    PARTNER_BM_ID = business_id  # OQ business id
    res = get_all_businesses_by_user_id(client_admin_access_token, client_user_id)
    if res.get('status') != 200:
        return res
    BMs_id_list = list()

    BMs_in_DB = list()
    for BM_record in db.getFB_CLIENT_BM_IDS_BY_OQ_USER_ID(oq_user_id):
        BMs_in_DB.append(BM_record[1])

    for BM in res.get('body').get('businesses').get('data'):  # get all businesses belong to user
        if BM.get('id') == str(PARTNER_BM_ID):
            continue
        BMs_id_list.append(BM.get('id'))
    # CLIENT_BM_ID = res.get('body').get('data')[1].get('id') # todo: allow client user to choose client BM id.

    succeeded_BMs_id_list = ""

    for CLIENT_BM_ID in BMs_id_list:
        # *** GET ALL BUSINESS ASSETS ***
        ASSETS_IDS = list()  # todo: allow client user to choose assets that belong to his business.
        res = get_all_business_assets(client_admin_access_token, CLIENT_BM_ID)
        if res.get('status') != 200:
            return res
        owned_ad_accounts_ids = list()
        if (res.get('body') is None) or (res.get('body').get('owned_ad_accounts') is None) or (
                res.get('body').get('owned_ad_accounts').get('data') is None):
            continue

        for ad_account in res.get('body').get('owned_ad_accounts').get('data'):
            owned_ad_accounts_ids.append(ad_account.get('id'))
            ASSETS_IDS.append(ad_account.get('id'))

        owned_pages_ids = list()
        for page in res.get('body').get('owned_pages').get('data'):
            owned_pages_ids.append(page.get('id'))
            ASSETS_IDS.append(page.get('id'))

        # *** STEP 1 ***
        # This creates an relationship edge between partner's Business Manager and client's Business Manager.
        # This enables the partner to be able to create a SU via the API in the next step

        params = {
            'existing_client_business_id': CLIENT_BM_ID,
            'access_token': client_admin_access_token
        }
        res = requests.post('https://graph.facebook.com/v13.0/' + str(PARTNER_BM_ID) + '/managed_businesses', params)
        if res.status_code != 200:
            return {"status": res.status_code, "body": res.json()}

        # *** STEP 2 ***
        # Fetch the access token of system user under the client's Business Manager
        PARTNER_BM_ADMIN_SYSTEM_USER_ACCESS_TOKEN = client_admin_access_token  # fixed! todo: fetch PARTNER_BM_ADMIN_SYSTEM_USER_ACCESS_TOKEN

        params = {
            'scope': "ads_management,pages_read_engagement,ads_read,business_management",
            'app_id': str(OQ_app_id),
            'access_token': PARTNER_BM_ADMIN_SYSTEM_USER_ACCESS_TOKEN
        }
        res = requests.post('https://graph.facebook.com/v13.0/' + CLIENT_BM_ID + '/access_token', params)
        if res.status_code != 200:
            return {"status": res.status_code, "body": res.json()}

        # The response contains the token for the system user who is linked to the On Behalf Of relationships.
        CLIENT_BM_SU_ACCESS_TOKEN = res.json().get('access_token')  # fixed! todo: get this system user token

        # *** STEP 3 ***
        # Get the ID of the system user.
        params = {
            'access_token': CLIENT_BM_SU_ACCESS_TOKEN
        }
        res = requests.get('https://graph.facebook.com/v13.0/me', params)
        if res.status_code != 200:
            return {"status": res.status_code, "body": res.json()}
        SYSTEM_USER_ID = res.json().get('id')

        # *** STEP 4 ***
        # Assign assets to the system user in the client's Business Manager.
        ad_accounts_in_DB = list()
        for ad_account_record in db.getFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(CLIENT_BM_ID):
            ad_accounts_in_DB.append(ad_account_record[1])

        pages_in_DB = list()
        for page_record in db.getFB_CLIENT_PAGES_BY_BM_ID(CLIENT_BM_ID):
            pages_in_DB.append(page_record[1])

        for asset in owned_ad_accounts_ids:
            params = {
                "user": SYSTEM_USER_ID,
                "tasks": "MANAGE",
                'access_token': client_admin_access_token
            }
            # time.sleep(2)
            res = requests.post('https://graph.facebook.com/v13.0/' + asset + '/assigned_users', params)
            if res.status_code != 200:
                return {"status": res.status_code, "body": res.json()}
            if asset not in ad_accounts_in_DB:
                db.addFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(CLIENT_BM_ID, asset)

        for asset in owned_pages_ids:
            params = {
                "user": SYSTEM_USER_ID,
                "tasks": "MANAGE",
                'access_token': client_admin_access_token
            }
            # time.sleep(2)
            res = requests.post('https://graph.facebook.com/v13.0/' + asset + '/assigned_users', params)
            if res.status_code != 200:
                return {"status": res.status_code, "body": res.json()}
            if asset not in pages_in_DB:
                db.addFB_CLIENT_PAGES_BY_BM_ID(CLIENT_BM_ID, asset)

        owned_pixels_ids = list()
        pixels_res = get_all_business_pixels(client_admin_access_token, CLIENT_BM_ID)
        if pixels_res.status_code != 200:
            return {"status": pixels_res.status_code, "body": pixels_res.json()}

        print("pixels_res: " + str(pixels_res.json()))

        if (pixels_res.json() is not None) and (pixels_res.json().get('owned_pixels') is not None) and (
                pixels_res.json().get('owned_pixels').get('data') is not None):
            for pixel in pixels_res.json().get('owned_pixels').get('data'):
                owned_pixels_ids.append(pixel.get('id'))
                ASSETS_IDS.append(pixel.get('id'))

        for asset in owned_pixels_ids:
            params = {
                "user": SYSTEM_USER_ID,
                "tasks": "EDIT, ANALYZE, UPLOAD, ADVERTISE, AA_ANALYZE",
                'access_token': client_admin_access_token
            }
            # time.sleep(2)
            res = requests.post('https://graph.facebook.com/v13.0/' + asset + '/assigned_users', params)
            if res.status_code != 200:
                return {"status": res.status_code, "body": res.json()}
            # if asset not in pages_in_DB: #todo
            #     db.addFB_CLIENT_PAGES_BY_BM_ID(CLIENT_BM_ID, asset)

        if CLIENT_BM_ID not in BMs_in_DB:
            db.addFB_CLIENT_BM_SU_ACCESS_TOKEN(oq_user_id, CLIENT_BM_ID, str(PARTNER_BM_ID), client_user_id,
                                               CLIENT_BM_SU_ACCESS_TOKEN)
        succeeded_BMs_id_list += CLIENT_BM_ID + ","

    # ** DONE: **
    # todo: save CLIENT_BM_SU_ACCESS_TOKEN in DB
    #  primary key: user ID is OQ system. save also FB_uid. save also CLIENT_BM_SU_ACCESS_TOKEN

    if len(succeeded_BMs_id_list) == 0:
        return {"status": 400, "body": {"No business added as a client"}}

    return {"status": 200, "body": {"client_businesses_added": succeeded_BMs_id_list}}
