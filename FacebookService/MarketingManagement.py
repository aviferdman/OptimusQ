import time

import requests
import urllib.request
from DataBaseService.main import dataBaseController

import base64
import io

# This interface allows the user to create and manage all the marketing fields,
# using Facebook APIs.
from FacebookService import AdAccount, Campaign, AdSet, AdCreative, Image, Ad, Insights, Pixel, Business

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
    return AdAccount.create_ad_account(access_token, business_id, account_name, currency, timezone_id,
                      end_advertiser, media_agency, partner)


# get ad account by id
def get_ad_account_by_id(access_token, ad_account_id):
    return AdAccount.get_ad_account_by_id(access_token, ad_account_id)


# returns all ad accounts belong to business_id
def get_all_ad_accounts_in_business(access_token, business_id):
    return AdAccount.get_all_ad_accounts_in_business(access_token, business_id)


# creates a new campaign.
# all params are string. special_ad_categories in the form: "[]"
# returns: new campaign's id
def create_new_campaign(access_token, ad_account_id, campaign_name, objective="LINK_CLICKS",
                        status="PAUSED", special_ad_categories="[]"):
    return Campaign.create_new_campaign(access_token, ad_account_id, campaign_name, objective,
                        status, special_ad_categories)


# returns a campaign by id
def get_campaign_by_id(access_token, campaign_id):
    return Campaign.get_campaign_by_id(access_token, campaign_id)


# returns all campaign belongs to AD_ACCOUNT_ID
def get_all_campaigns(access_token, ad_account_id):
    return Campaign.get_all_campaigns(access_token, ad_account_id)


# creates a new ad set
def create_new_ad_set(access_token, AD_ACCOUNT_ID, ad_set_name, campaign_id, daily_budget="1000",
                      optimization_goal='REACH',
                      billing_event='IMPRESSIONS', bid_amount="1500",
                      start_time='1633851746', status='PAUSED',
                      targeting_min_age='NONE', targeting_max_age='NONE', targeting_countries=["IL"], end_time='NONE',
                      targeting_gender="NONE", targeting_relationship_statuses="NONE",
                      targeting_interests=[], targeting_behaviors=[], promoted_object=None):
    return AdSet.create_new_ad_set(access_token, AD_ACCOUNT_ID, ad_set_name, campaign_id, daily_budget,
                      optimization_goal,
                      billing_event, bid_amount,
                      start_time, status,
                      targeting_min_age, targeting_max_age, targeting_countries, end_time,
                      targeting_gender, targeting_relationship_statuses,
                      targeting_interests, targeting_behaviors, promoted_object)


# returns all ad sets belongs to AD_ACCOUNT_ID
def get_all_ad_sets_by_ad_account(access_token, ad_account_id, with_status="['ACTIVE', 'PAUSED']"):
    return AdSet.get_all_ad_sets_by_ad_account(access_token, ad_account_id, with_status)


# returns all ad sets belongs to campaign with campaign_id
def get_all_ad_sets_by_campaign(access_token, campaign_id):
    return AdSet.get_all_ad_sets_by_campaign(access_token, campaign_id)


# returns all ad creatives belongs to ad account
def get_all_ad_creatives(access_token, ad_account):
    return AdCreative.get_all_ad_creatives(access_token, ad_account)


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_path(access_token, AD_ACCOUNT_ID, image_path):
    return Image.upload_image_by_path(access_token, AD_ACCOUNT_ID, image_path)


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_url(access_token, AD_ACCOUNT_ID, image_url):
    return Image.upload_image_by_url(access_token, AD_ACCOUNT_ID, image_url)


# returns a A permanent URL of the image
def get_permanent_url_for_image_by_hash(access_token, ad_account, hash):
    return Image.get_permanent_url_for_image_by_hash(access_token, ad_account, hash)


# creates a new ad creative
def create_ad_creative(access_token, name, image_hash, ad_account_id, link, message, page_id='107414948611212'):
    return AdCreative.create_ad_creative(access_token, name, image_hash, ad_account_id, link, message, page_id)


# creates an ad of type "carousel"
# todo: make this function generic
def create_carousel_ad(access_token, name, image_hash, link, description, page_id='107414948611212'):
    return AdCreative.create_carousel_ad(access_token, name, image_hash, link, description, page_id)


# creates a new ad
def create_ad(access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status="PAUSED"):
    return Ad.create_ad(access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status)


# get all ads by ad account
def get_all_ads_by_adAcount_id(access_token, ad_account_id):
    return Ad.get_all_ads_by_adAcount_id(access_token, ad_account_id)


# get all ads by campaign
def get_all_ads_by_campaign_id(access_token, campaign_id):
    return Ad.get_all_ads_by_campaign_id(access_token, campaign_id)


# get all ads by adSet id
def get_all_ads_by_adSet_id(access_token, adSet_id):
    return Ad.get_all_ads_by_adSet_id(access_token, adSet_id)


# get an adCreative preview
def get_adCreative_preview(access_token, creative_id, ad_format='DESKTOP_FEED_STANDARD'):
    return AdCreative.get_adCreative_preview(access_token, creative_id, ad_format)


# get an ad preview
def get_ad_preview(access_token, ad_id, ad_format='DESKTOP_FEED_STANDARD'):
    return AdCreative.get_ad_preview(access_token, ad_id, ad_format)


# You cannot remove ad accounts from your business if you're OWNER and if the accounts are CONFIRMED.
# If you have a PENDING access request or you have AGENCY access to the ad account, you can make this DELETE call
def delete_ad_account(access_token, business_id, ad_account_id):
    return AdAccount.delete_ad_account(access_token, business_id, ad_account_id)


# returns: success: bool
def delete_campaign(access_token, campaign_id):
    return Campaign.delete_campaign(access_token, campaign_id)


# returns: success: bool
def delete_adSet(access_token, adSet_id):
    return AdSet.delete_adSet(access_token, adSet_id)


# returns: success: bool
def delete_ad_creative(access_token, ad_creative_id):
    return AdCreative.delete_ad_creative(access_token, ad_creative_id)


# returns: success: bool
def delete_ad(access_token, ad_id):
    return Ad.delete_ad(access_token, ad_id)


# get insights for ad account/campaign/ad set/ ad
def get_insights(access_token, marketing_object_id, date_preset='maximum'):
    return Insights.get_insights(access_token, marketing_object_id, date_preset)


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
    return Business.get_all_client_BMs_by_oq_user_id(oq_user_id)


def get_all_client_ad_accounts_by_BM_id(BM_id):
    return Business.get_all_client_ad_accounts_by_BM_id(BM_id)


def get_all_client_pages_by_BM_id(BM_id):
    return Business.get_all_client_pages_by_BM_id(BM_id)


# get token for client by oq user id
def get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id):
    return Business.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)


# returns all businesses by user id: id and name
def get_all_businesses_by_user_id(access_token, user_id):
    return Business.get_all_businesses_by_user_id(access_token, user_id)


# returns all business asset groups
def get_all_business_asset_groups(access_token, business_id):
    return Business.get_all_business_asset_groups(access_token, business_id)


# returns all ASSETS_IDS for a business, for use in function create_on_behalf_of_relationship
def get_all_business_assets(access_token, business_id):
    return Business.get_all_business_assets(access_token, business_id)


# returns all pixels ids for business
def get_all_business_pixels(access_token, business_id):
    return Pixel.get_all_business_pixels(access_token, business_id)


# returns all pixels for ad account
def get_all_ad_account_pixels(access_token, ad_account_id):
    return Pixel.get_all_ad_account_pixels(access_token, ad_account_id)


# Create the On Behalf Of relationship between the partner and client's Business Manager.
# access token must be the user's and received by FB login - and not the app token.
# API tutorial for this function:
# https://developers.facebook.com/docs/marketing-api/business-manager/guides/on-behalf-of
# ASSETS_IDS is a list, containing assets ids for assigning from client BM to partner BM
def create_on_behalf_of_relationship(client_admin_access_token, client_user_id, oq_user_id):
    return Business.create_on_behalf_of_relationship(client_admin_access_token, client_user_id, oq_user_id)
