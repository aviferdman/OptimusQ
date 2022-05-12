# This file is responsible for the UI.
# It is directly linked to any change we make in the business layer.
# That is, we can conveniently send a URL and see if what we expected to receive was received.

# 'Flask' is a library of web applications written in Python.
from doctest import OutputChecker
import json
from flask import Flask, render_template, request, flash, Markup, jsonify, redirect
import time
import requests

from DataBaseService.main import DataBaseController, dataBaseController
# deleteAccessTokenByUserId, writeAccessToken2db, getAccessTokenByUserId

from FacebookService import MarketingManagement
# from GoogleAdsService import CampaignManagement
# from GoogleAdsService2 import CampaignManagement

from PresentationService.main import main_trigger

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

db = dataBaseController
sandbox_token = db.getAccessTokenByUserId('sandbox_token')
admin_token = db.getAccessTokenByUserId('admin_token')


@app.route("/")
def hello():
    """
    purpose: Displays on the screen the home page where the user can enter a URL
    :param : None
    :return: HTML page
    """
    return render_template("main_index.html")


@app.route("/fb_login")
def fb_login():
    """
    purpose: Displays on the screen the home page where the user can enter a URL
    :param : None
    :return: HTML page
    """
    return render_template("fb_login.html")


@app.route("/fb")
def fb_index():
    """
    purpose: Displays on the screen the home page where the user can enter a URL
    :param : None
    :return: HTML page
    """
    return render_template("fb_index.html")


@app.route("/extract_kw")
def extract_kw():
    """
    purpose: Displays on the screen the home page where the user can enter a URL
    :param : None
    :return: HTML page
    """
    return render_template("extract_kw.html")


@app.route("/fb_login_handler", methods=['POST', 'GET'])
def fb_login_handler():
    return render_template("fb_logged_in.html")


@app.route("/fb_logged_in", methods=['POST', 'GET'])
def fb_logged_in():
    res_preview = ""
    if request.method == "POST":
        print("POST!!!: ")
        rq = request.get_json()
        user_id = rq["user_id"]
        access_token = rq["access_token"]
        access_token = admin_token
        print("user_id: " + user_id)
        ad_accounts = [{'account_id': '1394987677611796'}]
        # ad_accounts_list = MarketingManagement.get_all_ad_accounts_in_business(access_token).json()
        campaigns = []
        ad_sets = []

        # ad_account_id = account['id'][4::] # only the id, without the prefix of act_
        ad_account_id = '1394987677611796'
        campaigns = campaigns + (
        MarketingManagement.get_all_campaigns(access_token, ad_account_id).get('body').get('campaigns').get("data"))
        ad_sets = ad_sets + (
        MarketingManagement.get_all_ad_sets_by_ad_account(access_token, ad_account_id).json()['data'])
        ads = []
        ad_preview = {}
        res_preview = ""
        # preview = MarketingManagement.get_ad_preview(access_token, '120330000358031413').get('body').get('data')[0].get('body')
        # print(preview)
        # flash(Markup(preview))
        # for ad_set in ad_sets:
        #     ad_set_id = ad_set['id']
        ads = ads + (MarketingManagement.get_all_ads_by_adSet_id(access_token, '23850154047300253').get('body').get('data'))
        # ads = ads[0:6]
        # count = 0
        for ad in ads:
            # if count > 5:
            #     break
            # count += 1
            preview = MarketingManagement.get_ad_preview(access_token, ad.get('id')).get('body').get('data')[0].get('body')
            ad_id = ad.get('id')
            res_preview += "id: " + ad_id + ", name: " + ad['name'] + "<br>preview:<br>" + preview + "<br><br>"
            ad_preview[ad_id] = preview
    list_of_images = []
    list_of_images.append("1")
    list_of_images.append("2")
    flash(Markup(res_preview))
    return render_template("fb_logged_in.html",
                           output={"ad_accounts": ad_accounts, "campaigns": campaigns, "ad_sets": ad_sets, "ads": ads, "ad_preview": ad_preview})
    # return render_template("fb_logged_in.html", output=list_of_images)


@app.route("/create_ad", methods=['POST', 'GET'])
def create_ad_set_automatically():
    """
    created an ad set automatically by a landing page url
    """
    if request.method == "POST":
        print("POST FROM create_ad!!!: ")
        rq = request.get_json()
        print("request: " + str(rq))
        access_token = rq["access_token"]
        ad_account = rq["ad_account"]
        url = rq["url"]  # image url
        ad_link = rq["ad_link"]
        ad_body = rq["ad_body"]
        ad_name = rq["ad_name"]
        campaign = rq["campaign"]
        # print(MarketingManagement.create_new_ad_set(
        #     ad_account, adset_name, access_token, campaign, daily_budget
        # ).json())
        # img_hashes = []
        # for img_url in list_of_images:
        #     print(MarketingManagement.upload_image_by_url(ad_account, access_token, img_url).json())
        #     time.sleep(6)
        # MarketingManagement.upload_image_by_url(ad_account, access_token, img_url).json()["images"]["bytes"]["hash"]
        img_hash = MarketingManagement.upload_image_by_url(admin_token, '1394987677611796', url).get('body').get('images').get('bytes').get('hash')
        print('img_hash: ' + img_hash)
        creative_id = MarketingManagement.create_ad_creative(admin_token, "creative name", img_hash, '1394987677611796', ad_link, ad_body).get('body').get('id')
        print('creative_id: ' + creative_id)
        res = MarketingManagement.create_ad(admin_token, '1394987677611796', ad_name, '23850154047300253', creative_id).get('body').get('id')
        print('ad id: ' + res)
        print('ad created id: ' + res)

        # for img_hash in img_hashes:
        #     MarketingManagement.create_ad_creative("default name", access_token, img_hash)

    # url = str(request.form['url'])
    # print("url:" + url)

    # adset_name = str(request.form['adset_name'])
    # daily_budget = str(request.form['daily_budget'])
    # ad_account = str(request.form['ad_account'])
    # print("ad account:" + ad_account)
    # print("adset_name:" + adset_name)
    # print("daily_budget:" + daily_budget)
    ad_accounts = ["123"]
    return redirect("/fb_logged_in")


@app.route("/create_ad_set_form", methods=['POST', 'GET'])
def create_ad_set_form():
    """
    created an ad set form
    """
    ad_accounts = ["123"]
    campaigns = []
    return render_template("extract_kw.html", output2=ad_accounts)
    # output2 = {"ad_accounts": ad_accounts}
    # return output2


@app.route("/extract_data", methods=['POST', 'GET'])
def extract_keywords_from_landing_page():
    """
    purpose: Displays on-screen the information extracted from the entered URL
    :param : None
    :return: HTML page
    """
    # receive URL and check if valid
    url = str(request.form['url'])
    if url == "":
        flash("Please enter a valid url")
        return render_template("main_index.html")
    result = main_trigger(url)  # Contains a dictionary with all the information extracted
    if result["title"] == "can't open the url":
        flash("can't open url")
        return render_template("main_index.html")
    if not result:
        flash("can't extract the data from this url... working on it:)")
        return render_template("main_index.html")
    images = result["images"]
    list_of_images = []
    for k in images.keys():
        if images[k]:
            list_of_images.append(images[k][0])

    # Text created that will be displayed on the screen after extracting the information
    res_txt = "<b>Title: </b><br>"
    res_txt += result["title"]
    res_txt += "<br>"
    res_txt += "<br><b>Description:</b><br>"
    res_txt += result["description"]
    res_txt += "<br><br><b>Keywords:</b><br>"
    keywords_count = 0
    for kw in result["keywords"]:
        if keywords_count > 4:
            break
        keywords_count += 1
        res_txt += kw + "<br>"
    res_txt += "<br><b>Recommended Images:</b>"
    flash(Markup(res_txt))
    return render_template("extract_kw.html", output=list_of_images)


@app.route("/api/fb/save_in_db", methods=['POST', 'GET'])
def save_in_db():
    if request.method == "POST":
        print("POST to DB!!!: ")
        rq = request.get_json()
        # db = dataBaseController
        print("inserting to db...")
        db.writeAccessToken2db(rq["user_id"], rq["token"])
        return "success"


# get_all_campaigns
@app.route("/api/fb/get_all_campaigns", methods=['GET'])
def fb_api_get_all_campaigns():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account = rq['ad_account']
        token = db.getAccessTokenByUserId('sandbox_token')
        return MarketingManagement.get_all_campaigns(token, ad_account)

# upload_img_from_url
@app.route("/api/fb/upload_img_from_url", methods=['POST'])
def upload_img_from_url():
    if request.method == "POST":
        print("upload_img_from_url: POST!")
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account_id = rq['ad_account']
        img_url = rq['img_url']
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.upload_image_by_url(token, ad_account_id, img_url)
        try:
            img_hash = res.get('body').get('images').get('bytes').get('hash')
            res2 = MarketingManagement.get_permanent_url_for_image_by_hash(token, ad_account_id, img_hash)
            img_permalink_url = res2.get('body').get('data')[0].get('permalink_url')
            db.addFBImage(img_hash, img_permalink_url)
        except Exception as e:
            print(str(e))
        return res

# get_all_ad_sets_for_campaign
@app.route("/api/fb/get_all_ad_sets_by_campaign", methods=['GET'])
def fb_api_get_all_ad_sets_by_campaign():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        campaign_id = rq['campaign_id']
        token = db.getAccessTokenByUserId('sandbox_token')
        return MarketingManagement.get_all_ad_sets_by_campaign(token, campaign_id)

@app.route("/api/fb/upload_image_by_path", methods=['POST'])
def fb_api_upload_image_by_path():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account_id = rq['ad_account']
        img_url = rq['img_url']
        token = db.getAccessTokenByUserId('sandbox_token')
        return MarketingManagement.upload_image_by_url(ad_account_id, token, img_url)


@app.route("/api/fb/create_adCreative", methods=['POST'])
def create_adCreative():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account_id = rq['ad_account']
        name = rq['name']
        img_hash = rq['img_hash']
        link = rq['link']
        msg = rq['msg']
        page_id = rq['page_id']
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.create_ad_creative(token, name, img_hash, ad_account_id, link, msg, page_id)
        if res.get('status') == 200:
            try:
                db.addFBAdCreative(res.get('body').get('id'), name, page_id, msg, img_hash)
            except Exception as e:
                print(str(e))
        return res

@app.route("/api/fb/create_ad", methods=['POST'])
def create_ad():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account_id = rq['ad_account']
        name = rq['name']
        adset = rq['adset']
        creative = rq['creative']
        status = rq['status']
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.create_ad(token, ad_account_id, name, adset, creative, status)
        if res.get('status') == 200:
            try:
                ad_id = res.get('body').get('id')
                db.addFBAd(ad_id, adset, name, creative, status)
            except Exception as e:
                print(str(e))
        return res

@app.route("/api/fb/create_new_adset", methods=['POST'])
def create_new_adset():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account_id = rq['ad_account']
        ad_set_name = rq['ad_set_name']
        campaign_id = rq['campaign_id']
        daily_budget = '1000'
        if 'daily_budget' in rq:
            daily_budget = rq['daily_budget']
        optimization_goal = 'REACH'
        if 'optimization_goal' in rq:
            optimization_goal = rq['optimization_goal']
        billing_event = 'IMPRESSIONS'
        if 'billing_event' in rq:
            billing_event = rq['billing_event']
        targeting = {"geo_locations": {"countries": ["US"]}}
        if 'targeting' in rq:
            targeting = rq['targeting']
        bid_amount = '1500'
        if 'bid_amount' in rq:
            bid_amount = rq['bid_amount']
        start_time = '2020-10-06T04:45:17+0000'
        if 'start_time' in rq:
            start_time = rq['start_time']
        status = 'PAUSED'
        if status in rq:
            status = rq['status']
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.create_new_ad_set(token, ad_account_id, ad_set_name, campaign_id, daily_budget,
                                                     optimization_goal, billing_event, bid_amount, targeting, start_time, status)
        if res.get('status') == 200:
            try:
                adset_id = res.get('body').get('id')
                db.addAdSet(adset_id, ad_account_id, campaign_id, ad_set_name, daily_budget, 'targeting')
            except Exception as e:
                print(str(e))
        return res


# create_new_campaign
@app.route("/api/fb/create_new_campaign", methods=['POST'])
def fb_api_create_new_campaign():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_account_id = rq['ad_account']
        campaign_name = rq.get('campaign_name')
        objective = rq.get('objective', 'LINK_CLICKS')
        status = rq.get('status', 'PAUSED')
        special_ad_categories = rq.get('special_ad_categories', "[]")
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.create_new_campaign(token, ad_account_id, campaign_name, objective, status, special_ad_categories)
        if res.get('status') == 200:
            try:
                campaign_id = res.get('body').get('id')
                db.addCampaign(campaign_id, ad_account_id, campaign_name, objective, status)
            except Exception as e:
                print(str(e))
        return res

# get_ad_preview
@app.route("/api/fb/get_ad_preview", methods=['GET'])
def fb_api_get_ad_preview():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_id = rq['ad_id']
        ad_format = rq.get('ad_format', 'DESKTOP_FEED_STANDARD')
        token = db.getAccessTokenByUserId('sandbox_token')
        return MarketingManagement.get_ad_preview(token, ad_id, ad_format)

# get all ads by adSet
@app.route("/api/fb/get_all_ads_by_adSet_id", methods=['GET'])
def fb_api_get_all_ads_by_adSet_id():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        adset_id = rq['adset_id']
        token = db.getAccessTokenByUserId('sandbox_token')
        return MarketingManagement.get_all_ads_by_adSet_id(token, adset_id)

# get insights for ad account/campaign/ad set/ad
@app.route("/api/fb/get_insights", methods=['GET'])
def fb_api_get_insights():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        marketing_object_id = rq['marketing_object_id']
        date_preset = rq.get('date_preset', 'maximum')
        token = db.getAccessTokenByUserId('sandbox_token')
        return MarketingManagement.get_insights(token, marketing_object_id, date_preset)
      

# deletes a campaign
@app.route("/api/fb/campaigns", methods=['DELETE'])
def fb_api_delete_campaign():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        campaign_id = rq.get('campaign_id', '-1')
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.delete_campaign(token, campaign_id)
        if res.get('status') == 200:
            try:
                db.deleteCampaign(campaign_id)
            except Exception as e:
                print(str(e))
        return res


# deletes an ad set
@app.route("/api/fb/adsets", methods=['DELETE'])
def fb_api_delete_adSet():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        adset_id = rq.get('adset_id', '-1')
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.delete_adSet(token, adset_id)
        if res.get('status') == 200:
            try:
                db.deleteAdSet(adset_id)
            except Exception as e:
                print(str(e))
        return res

# deletes an ad creative
@app.route("/api/fb/ad_creatives", methods=['DELETE'])
def fb_api_delete_ad_creative():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        creative_id = rq.get('creative_id', '-1')
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.delete_ad_creative(token, creative_id)
        if res.get('status') == 200:
            try:
                db.deleteFBAdCreative(creative_id)
            except Exception as e:
                print(str(e))
        return res


# deletes an ad
@app.route("/api/fb/ads", methods=['DELETE'])
def fb_api_delete_ad():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        ad_id = rq.get('ad_id', '-1')
        token = db.getAccessTokenByUserId('sandbox_token')
        res = MarketingManagement.delete_ad(token, ad_id)
        if res.get('status') == 200:
            try:
                db.deleteFBAd(ad_id)
            except Exception as e:
                print(str(e))
        return res



################################################## Google-Ads ##########################################################
#
# #todo add try and catch
# # create_new_campaign
# @app.route("/api/GoogleAds/create_new_campaign", methods=['GET', 'POST'])
# def googleAds_api_create_new_campaign():
#     if request.method == "POST":
#         rq = request.get_json(force=True)
#         customer_id = rq.get('customer_id')
#         budget = rq.get('budget')
#         name = rq.get('name')
#         days_to_start = rq.get('days_to_start')
#         weeks_to_end = rq.get('weeks_to_end')
#         status = rq.get('status', 'PAUSED')
#         res = CampaignManagement.create_new_campaign(customer_id, budget, name, days_to_start, weeks_to_end, status)
#        # try:
#        #      campaign_id = res.get('body').get('id')
#        #      db.addCampaign(campaign_id, ad_account_id, campaign_name, objective, status)
#        #  except Exception as e:
#        #      print(str(e))
#         return res
#
# # get_all_campaigns
# @app.route("/api/GoogleAds/get_all_campaigns", methods=['GET'])
# def googleAds_api_get_all_campaigns():
#     if request.method == "GET":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         return CampaignManagement.get_all_campaigns(customer_id)
#
# # get_campaign_by_id
# @app.route("/api/GoogleAds/get_campaign", methods=['GET'])
# def googleAds_api_get_campaign_by_id():
#     if request.method == "GET":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         campaign_id = rq['campaign_id']
#         return CampaignManagement.get_campaign_by_id(customer_id, campaign_id)
#
# # delete_campaign
# @app.route("/api/GoogleAds/delete_campaign", methods=['DELETE'])
# def googleAds_api_delete_campaign():
#     if request.method == "DELETE":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         campaign_id = rq['campaign_id']
#         res = CampaignManagement.delete_campaign(customer_id, campaign_id)
#         # if res.get('status') == 200:
#         #     try:
#         #         db.deleteFBAd(ad_id)
#         #     except Exception as e:
#         #         print(str(e))
#         return res
#
# # create_new_ad_group
# @app.route("/api/GoogleAds/create_new_ad_group", methods=['POST'])
# def googleAds_api_create_new_ad_group():
#     if request.method == "POST":
#         rq = request.get_json(force=True)
#         customer_id = rq.get('customer_id')
#         campaign_id = rq.get('campaign_id')
#         name = rq.get('name')
#         cpc_bid = rq.get('cpc_bid')   # cost per click in IL shekels
#         status = rq.get('status', 'ENABLED')
#         res = CampaignManagement.create_new_adgroup(customer_id, campaign_id, name, status, cpc_bid)
#             # try:
#             #     adset_id = res.get('body').get('id')
#             #     db.addAdSet(adset_id, ad_account_id, campaign_id, ad_set_name, daily_budget, 'targeting')
#             # except Exception as e:
#             #     print(str(e))
#         return res
#
# # get_all_ad_groups
# @app.route("/api/GoogleAds/get_all_ad_groups", methods=['GET'])
# def googleAds_api_get_all_ad_groups():
#     if request.method == "GET":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         campaign_id = rq.get('campaign_id')
#         return CampaignManagement.get_all_ad_groups(customer_id, campaign_id)
#
# # delete_ad_group
# @app.route("/api/GoogleAds/delete_ad_group", methods=['DELETE'])
# def googleAds_api_delete_ad_group():
#     if request.method == "DELETE":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         ad_group_id = rq['ad_group_id']
#         res = CampaignManagement.delete_ad_group(customer_id, ad_group_id)
#         # if res.get('status') == 200:
#         #     try:
#         #         db.deleteFBAd(ad_id)
#         #     except Exception as e:
#         #         print(str(e))
#         return res
#
# # add a keyword to ad group
# @app.route("/api/GoogleAds/add_keyword", methods=['POST'])
# def googleAds_api_add_keyword():
#     if request.method == "POST":
#         rq = request.get_json(force=True)
#         customer_id = rq.get('customer_id')
#         ad_group_id = rq.get('ad_group_id')
#         keyword_text = rq.get('keyword_text')
#         res = CampaignManagement.add_keyword(customer_id, ad_group_id, keyword_text)
#             # try:
#             #     adset_id = res.get('body').get('id')
#             #     db.addAdSet(adset_id, ad_account_id, campaign_id, ad_set_name, daily_budget, 'targeting')
#             # except Exception as e:
#             #     print(str(e))
#         return res
#
# # get_keywords
# @app.route("/api/GoogleAds/get_keywords", methods=['GET'])
# def googleAds_api_get_keywords():
#     if request.method == "GET":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         ad_group_id = rq.get('ad_group_id')
#         return CampaignManagement.get_keywords(customer_id, ad_group_id)
#
# # delete_keyword
# @app.route("/api/GoogleAds/delete_keyword", methods=['DELETE'])
# def googleAds_api_delete_keyword():
#     if request.method == "DELETE":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         ad_group_id = rq['ad_group_id']
#         criterion_id = rq['criterion_id']
#         res = CampaignManagement.delete_keyword(customer_id, ad_group_id, criterion_id)
#         # if res.get('status') == 200:
#         #     try:
#         #         db.deleteFBAd(ad_id)
#         #     except Exception as e:
#         #         print(str(e))
#         return res
#
# # create_new_responsive_search_ad
# @app.route("/api/GoogleAds/create_new_RS_ad", methods=['POST'])
# def googleAds_api_create_new_RS_ad():
#     if request.method == "POST":
#         rq = request.get_json(force=True)
#         customer_id = rq.get('customer_id')
#         ad_group_id = rq.get('ad_group_id')
#         headlines_texts = rq.get('headlines_texts')
#         descriptions_texts = rq.get('descriptions_texts')
#         final_url = rq.get('final_url')
#         pinned_text = rq.get('pinned_text', None)
#         res = CampaignManagement.create_new_responsive_search_ad(customer_id, ad_group_id, headlines_texts, descriptions_texts, final_url, pinned_text)
#        # try:
#        #      campaign_id = res.get('body').get('id')
#        #      db.addCampaign(campaign_id, ad_account_id, campaign_name, objective, status)
#        #  except Exception as e:
#        #      print(str(e))
#         return res
#
# # get_all_responsive_search_ads
# @app.route("/api/GoogleAds/get_all_RS_ads", methods=['GET'])
# def googleAds_api_get_all_RS_ads():
#     if request.method == "GET":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         ad_group_id = rq.get('ad_group_id')
#         return CampaignManagement.get_all_responsive_search_ads(customer_id, ad_group_id)
#
# # delete_ad
# @app.route("/api/GoogleAds/delete_ad", methods=['DELETE'])
# def googleAds_api_delete_ad():
#     if request.method == "DELETE":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         ad_group_id = rq['ad_group_id']
#         ad_id = rq['ad_id']
#         res = CampaignManagement.delete_ad(customer_id, ad_group_id, ad_id)
#         # if res.get('status') == 200:
#         #     try:
#         #         db.deleteFBAd(ad_id)
#         #     except Exception as e:
#         #         print(str(e))
#         return res


# for running in local host with HTTP
if __name__ == '__main__':
    app.run()

# for running in local host with HTTPS
# first, create cert.pem and key.pem with the following cmd command:
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
# run with cmd command: python app.py
# if __name__ == '__main__':
#     app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
