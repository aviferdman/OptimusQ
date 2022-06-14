# This file is responsible for the UI.
# It is directly linked to any change we make in the business layer.
# That is, we can conveniently send a URL and see if what we expected to receive was received.

# 'Flask' is a library of web applications written in Python.
import threading
from doctest import OutputChecker
import json
from flask import Flask, render_template, request, flash, Markup, jsonify, redirect, session
import time
import requests

from DataBaseService.main import DataBaseController, dataBaseController
# deleteAccessTokenByUserId, writeAccessToken2db, getAccessTokenByUserId

from FacebookService import MarketingManagement
# from GoogleAdsService import CampaignManagement

from PresentationService.main import main_trigger

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

db = dataBaseController
sandbox_token = db.getAccessTokenByUserId('sandbox_token')
admin_token = db.getAccessTokenByUserId('admin_token')

# updates FB_targeting_behaviors DB once a week
threading.Thread(target=MarketingManagement.update_targeting_behaviors_once_a_week, args=(sandbox_token,)).start()


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
    oq_user_id = request.args.get('oq_user_id')
    session['oq_user_id'] = oq_user_id
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
        oq_user_id = session.get('oq_user_id', None)
        print("user_id: " + user_id)
        print("access_token: " + access_token)
        print("oq_user_id:" + oq_user_id)
        return MarketingManagement.create_on_behalf_of_relationship(access_token, user_id, oq_user_id)


@app.route("/api/fb/get_all_businesses_by_user_id", methods=['GET'])
def fb_api_get_all_businesses_by_user_id():
    if request.method == "GET":
        rq = request.get_json()
        user_id = rq["user_id"]
        access_token = rq["access_token"]
        print("user_id: " + user_id)
        print("access_token: " + access_token)
        return MarketingManagement.get_all_businesses_by_user_id(access_token, user_id)

@app.route("/api/fb/get_all_ad_accounts_in_business", methods=['GET'])
def fb_api_get_all_ad_accounts_in_business():
    if request.method == "GET":
        rq = request.get_json()
        business_id = rq["business_id"]
        access_token = rq["access_token"]
        return MarketingManagement.get_all_ad_accounts_in_business(access_token, business_id)





# @app.route("/fb_logged_in", methods=['POST', 'GET'])
# def fb_logged_in():
#     res_preview = ""
#     if request.method == "POST":
#         print("POST!!!: ")
#         rq = request.get_json()
#         user_id = rq["user_id"]
#         access_token = rq["access_token"]
#         print("user_id: " + user_id)
#         print("access_token: " + access_token)
#         ad_accounts = [{'account_id': '1394987677611796'}]
#         # ad_accounts_list = MarketingManagement.get_all_ad_accounts_in_business(access_token).json()
#         campaigns = []
#         ad_sets = []
#
#         # ad_account_id = account['id'][4::] # only the id, without the prefix of act_
#         ad_account_id = '1394987677611796'
#         campaigns = campaigns + (
#             MarketingManagement.get_all_campaigns(access_token, ad_account_id).get('body').get('campaigns').get("data"))
#         ad_sets = ad_sets + (
#             MarketingManagement.get_all_ad_sets_by_ad_account(access_token, ad_account_id).json()['data'])
#         ads = []
#         ad_preview = {}
#         res_preview = ""
#         # preview = MarketingManagement.get_ad_preview(access_token, '120330000358031413').get('body').get('data')[0].get('body')
#         # print(preview)
#         # flash(Markup(preview))
#         # for ad_set in ad_sets:
#         #     ad_set_id = ad_set['id']
#         ads = ads + (
#             MarketingManagement.get_all_ads_by_adSet_id(access_token, '23850154047300253').get('body').get('data'))
#         # ads = ads[0:6]
#         # count = 0
#         for ad in ads:
#             # if count > 5:
#             #     break
#             # count += 1
#             preview = MarketingManagement.get_ad_preview(access_token, ad.get('id')).get('body').get('data')[0].get(
#                 'body')
#             ad_id = ad.get('id')
#             res_preview += "id: " + ad_id + ", name: " + ad['name'] + "<br>preview:<br>" + preview + "<br><br>"
#             ad_preview[ad_id] = preview
#     list_of_images = []
#     list_of_images.append("1")
#     list_of_images.append("2")
#     flash(Markup(res_preview))
#     return render_template("fb_logged_in.html",
#                            output={"ad_accounts": ad_accounts, "campaigns": campaigns, "ad_sets": ad_sets, "ads": ads,
#                                    "ad_preview": ad_preview})
    # return render_template("fb_logged_in.html", output=list_of_images)

# create ad set automatically
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
        img_hash = MarketingManagement.upload_image_by_url(admin_token, '1394987677611796', url).get('body').get(
            'images').get('bytes').get('hash')
        print('img_hash: ' + img_hash)
        creative_id = MarketingManagement.create_ad_creative(admin_token, "creative name", img_hash, '1394987677611796',
                                                             ad_link, ad_body).get('body').get('id')
        print('creative_id: ' + creative_id)
        res = MarketingManagement.create_ad(admin_token, '1394987677611796', ad_name, '23850154047300253',
                                            creative_id).get('body').get('id')
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
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        ad_account = rq['ad_account']
        return MarketingManagement.get_all_campaigns(token, ad_account)

# get_all_campaigns
@app.route("/api/fb/get_all_campaigns_for_client", methods=['GET'])
def fb_api_get_all_campaigns_for_client():
    if request.method == "GET":
        rq = request.get_json()
        token = rq["token"]
        ad_account = rq["ad_account"]
        return MarketingManagement.get_all_campaigns(token, ad_account)

# uploads an image to DB
def upload_img_from_url_to_db(res, token, ad_account_id):
    try:
        img_hash = res.get('body').get('hash')
        res2 = MarketingManagement.get_permanent_url_for_image_by_hash(token, ad_account_id, img_hash)
        img_permalink_url = "Not Relevant"
        db.addFBImage(img_hash, img_permalink_url)
    except Exception as e:
        print(str(e))

# upload_img_from_url
@app.route("/api/fb/upload_img_from_url", methods=['POST'])
def upload_img_from_url():
    if request.method == "POST":
        print("upload_img_from_url: POST!")
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        
        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}

        ad_account_id = rq['ad_account']
        img_url = rq['img_url']
        res = MarketingManagement.upload_image_by_url(token, ad_account_id, img_url)
        if res.get('status') == 200:
            threading.Thread(target=upload_img_from_url_to_db, args=(res, token, ad_account_id,)).start()
        return res


# get_all_ad_sets_for_campaign
@app.route("/api/fb/get_all_ad_sets_by_campaign", methods=['GET'])
def fb_api_get_all_ad_sets_by_campaign():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token;
        campaign_id = rq['campaign_id']
        return MarketingManagement.get_all_ad_sets_by_campaign(token, campaign_id)


@app.route("/api/fb/upload_image_by_path", methods=['POST'])
def fb_api_upload_image_by_path():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token;
        ad_account_id = rq['ad_account']
        img_url = rq['img_url']
        return MarketingManagement.upload_image_by_url(ad_account_id, token, img_url)


@app.route("/api/fb/create_adCreative", methods=['POST'])
def create_adCreative():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token

        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}

        ad_account_id = rq['ad_account']
        name = rq['name']
        img_hash = rq['img_hash']
        link = rq['link']
        msg = rq['msg']
        page_id = rq.get('page_id')
        if (page_id is None) or (page_id == ''):
            page_id = '107414948611212'
        res = MarketingManagement.create_ad_creative(token, name, img_hash, ad_account_id, link, msg, page_id)
        if res.get('status') == 200:
            try:
                threading.Thread(target=db.addFBAdCreative, args=(res.get('body').get('id'), name, page_id, msg, img_hash)).start()
            except Exception as e:
                print(str(e))
        return res


@app.route("/api/fb/create_ad", methods=['POST'])
def create_ad():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token

        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}

        ad_account_id = rq['ad_account']
        name = rq['name']
        adset = rq['adset']
        creative = rq['creative']
        status = rq.get('status')
        if (status is None) or (status == ''):
            status = 'PAUSED'
        res = MarketingManagement.create_ad(token, ad_account_id, name, adset, creative, status)
        if res.get('status') == 200:
            try:
                ad_id = res.get('body').get('id')
                threading.Thread(target=db.addFBAd, args=(ad_id, adset, name, creative, status)).start()
            except Exception as e:
                print(str(e))
        return res


@app.route("/api/fb/create_new_adset", methods=['POST'])
def create_new_adset():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token

        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}

        promoted_object = rq.get("promoted_object")
        if promoted_object == "":
            promoted_object = None


        ad_account_id = rq.get('ad_account', '-1')
        ad_set_name = rq.get('ad_set_name', '-1')
        campaign_id = rq.get('campaign_id', '-1')
        daily_budget = '1000'
        if 'daily_budget' in rq:
            daily_budget = rq['daily_budget']
            if (daily_budget is None) or (daily_budget == -1):
                daily_budget = '1000'
        optimization_goal = 'REACH'
        if 'optimization_goal' in rq:
            optimization_goal = rq['optimization_goal']
            if (optimization_goal is None) or (optimization_goal == ""):
                optimization_goal = 'REACH'
        billing_event = 'IMPRESSIONS'
        if 'billing_event' in rq:
            billing_event = rq['billing_event']
            if (billing_event is None) or (billing_event == ""):
                billing_event = 'IMPRESSIONS'
        bid_amount = '1500'
        if 'bid_amount' in rq:
            bid_amount = rq['bid_amount']
            if (bid_amount is None) or (bid_amount == -1):
                bid_amount = '1500'
        start_time = '1633851746'
        if 'start_time' in rq:
            start_time = rq['start_time']
            if (start_time is None) or (start_time == ""):
                start_time = "1633851746"

        end_time = 'NONE'
        if 'end_time' in rq:
            end_time = rq['end_time']
            if (end_time is None) or (end_time == ""):
                end_time = "NONE"


        status = 'PAUSED'
        if status in rq:
            status = rq['status']
            if (status is None) or (status == ""):
                status = "PAUSED"
        targeting_gender = rq.get("targeting_gender")
        if (targeting_gender is None) or (targeting_gender == -1):
            targeting_gender = "NONE"
        if targeting_gender == -1:
            targeting_gender = "NONE"
        targeting_min_age = rq.get('targeting_min_age', 'NONE')
        if (targeting_min_age is None) or (targeting_min_age == -1):
            targeting_min_age = "NONE"
        targeting_max_age = rq.get('targeting_max_age', 'NONE')
        if (targeting_max_age is None) or (targeting_max_age == -1):
            targeting_max_age = "NONE"
        targeting_countries = []
        countries = rq.get('targeting_countries')
        if (countries is None) or (countries == ""):
            countries = 'IL'
        countries = countries.split(",")
        for country in countries:
            targeting_countries.append("" + country)

        targeting_interests_lst = []
        interests = rq.get('targeting_interests')
        if (interests is None) or (interests == ''):
            interests = []
        if len(interests) > 0:
            interests = interests.split(",")
            for interest_id in interests:
                targeting_interests_lst.append({"id": interest_id})

        behaviors = rq.get('targeting_behaviors')
        if (behaviors is None) or (behaviors == ''):
            behaviors = []
        targeting_behaviors_lst = []
        if len(behaviors) > 0:
            behaviors = behaviors.split(",")
            for behavior_id in behaviors:
                targeting_behaviors_lst.append({"id": behavior_id})

        targeting_relationships = []
        targeting_relationship_statuses = rq.get("targeting_relationship_statuses")
        if (targeting_relationship_statuses is None) or (targeting_relationship_statuses == ''):
            targeting_relationship_statuses = "NONE"
        else:
            statuses = targeting_relationship_statuses.split(",")
            for relationship_status in statuses:
                targeting_relationships.append(relationship_status)
        if len(targeting_relationships) == 0:
            targeting_relationships = "NONE"

        res = MarketingManagement.create_new_ad_set(token, ad_account_id, ad_set_name, campaign_id, daily_budget,
                                                    optimization_goal, billing_event, bid_amount, start_time, status,
                                                    targeting_min_age, targeting_max_age,
                                                    targeting_countries, end_time, targeting_gender,
                                                    targeting_relationships, targeting_interests_lst, targeting_behaviors_lst,
                                                    promoted_object)
        if res.get('status') == 200:
            try:
                adset_id = res.get('body').get('id')
                threading.Thread(target=db.addAdSet, args=(adset_id, ad_account_id, campaign_id, ad_set_name, daily_budget, 'targeting')).start()
            except Exception as e:
                print(str(e))
        return res


# create_new_campaign
@app.route("/api/fb/create_new_campaign", methods=['POST'])
def fb_api_create_new_campaign():
    if request.method == "POST":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token

        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}
        ad_account_id = rq['ad_account']
        campaign_name = rq.get('campaign_name')
        objective = rq.get('objective')
        if (objective is None) or (objective == ""):
            objective = "LINK_CLICKS"
        status = rq.get('status')
        if (status is None) or (status == ""):
            status = 'PAUSED'
        special_ad_categories = rq.get('special_ad_categories')
        if (special_ad_categories is None) or (len(special_ad_categories) == 0):
            special_ad_categories = "[]"
        else:
            special_ad_categories_lst = list()
            special_ad_categories_lst.append(special_ad_categories)
            special_ad_categories = special_ad_categories_lst

        res = MarketingManagement.create_new_campaign(token, ad_account_id, campaign_name, objective, status,
                                                      special_ad_categories)
        if res.get('status') == 200:
            try:
                campaign_id = res.get('body').get('id')
                threading.Thread(target=db.addCampaign, args=(campaign_id, ad_account_id, campaign_name, objective, status)).start()
            except Exception as e:
                print(str(e))
        return res


# get_ad_preview
@app.route("/api/fb/get_ad_preview", methods=['GET'])
def fb_api_get_ad_preview():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token

        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}
        
        ad_id = rq['ad_id']
        ad_format = rq.get('ad_format')
        if (ad_format is None) or (ad_format == ''):
            ad_format = 'DESKTOP_FEED_STANDARD'
        return MarketingManagement.get_ad_preview(token, ad_id, ad_format)


# get all ads by adSet
@app.route("/api/fb/get_all_ads_by_adSet_id", methods=['GET'])
def fb_api_get_all_ads_by_adSet_id():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        adset_id = rq['adset_id']
        return MarketingManagement.get_all_ads_by_adSet_id(token, adset_id)


# get insights for ad account/campaign/ad set/ad
@app.route("/api/fb/get_insights", methods=['GET'])
def fb_api_get_insights():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        marketing_object_id = rq['marketing_object_id']
        date_preset = rq.get('date_preset')
        if (date_preset is None) or (date_preset == ''):
            date_preset = 'maximum'
        return MarketingManagement.get_insights(token, marketing_object_id, date_preset)


# deletes a campaign
@app.route("/api/fb/campaigns", methods=['DELETE'])
def fb_api_delete_campaign():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        campaign_id = rq.get('campaign_id', '-1')
        res = MarketingManagement.delete_campaign(token, campaign_id)
        if res.get('status') == 200:
            try:
                threading.Thread(target=db.deleteCampaign, args=(campaign_id)).start()
            except Exception as e:
                print(str(e))
        return res


# deletes an ad set
@app.route("/api/fb/adsets", methods=['DELETE'])
def fb_api_delete_adSet():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        adset_id = rq.get('adset_id', '-1')
        res = MarketingManagement.delete_adSet(token, adset_id)
        if res.get('status') == 200:
            try:
                threading.Thread(target=db.deleteAdSet, args=(adset_id)).start()
            except Exception as e:
                print(str(e))
        return res


# deletes an ad creative
@app.route("/api/fb/ad_creatives", methods=['DELETE'])
def fb_api_delete_ad_creative():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token =""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        creative_id = rq.get('creative_id', '-1')
        res = MarketingManagement.delete_ad_creative(token, creative_id)
        if res.get('status') == 200:
            try:
                threading.Thread(target=db.deleteFBAdCreative, args=(creative_id)).start()
            except Exception as e:
                print(str(e))
        return res


# deletes an ad
@app.route("/api/fb/ads", methods=['DELETE'])
def fb_api_delete_ad():
    if request.method == "DELETE":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        ad_id = rq.get('ad_id', '-1')
        res = MarketingManagement.delete_ad(token, ad_id)
        if res.get('status') == 200:
            try:
                threading.Thread(target=db.deleteFBAd, args=(ad_id)).start()
            except Exception as e:
                print(str(e))
        return res

# search possible interests for ad targeting
@app.route("/api/fb/search_interests", methods=['GET'])
def fb_api_search_interests():
    if request.method == "GET":
        rq = request.get_json()
        is_sandbox_mode = rq['sandbox_mode']
        token = ""
        if (rq.get("to_search") is None) or (rq.get("to_search") == ""):
            return {'status': 400, 'body': 'to_search param cannot be null or empty string.'}
        if is_sandbox_mode == "no":
            return {'status': 400, 'body': 'currently working in sandbox mode only.'}
        else:
            token = sandbox_token
        res = MarketingManagement.search_for_possible_interests(token, rq.get("to_search", ""))
        return res

# search for behaviors in DB
@app.route("/api/fb/search_behaviors", methods=['GET'])
def fb_api_search_behaviors():
    if request.method == "GET":
        rq = request.get_json()
        to_search = rq.get("to_search", "")
        try:
            res = MarketingManagement.search_for_behaviors_in_db(to_search)
        except Exception as e:
            return {"status": 400, "body": {str(e)}}
        return {"status": 200, "body": {"data": res}}

# get all possible campaign objectives
@app.route("/api/fb/campaign_objectives", methods=['GET'])
def fb_api_get_all_possible_campaign_objectives():
    if request.method == "GET":
        return MarketingManagement.get_all_possible_campaign_objectives()

# get all optimization goals for objective
@app.route("/api/fb/optimization_goals_for_objective", methods=['GET'])
def fb_api_get_all_optimization_goals_for_objective():
    if request.method == "GET":
        rq = request.get_json()
        objective = rq.get("objective")
        if (objective is None) or (objective == ""):
            return {"status": 400, "body": "error: objective cannot be null or empty string"}
        if objective not in MarketingManagement.all_possible_campaign_objectives_lst:
            return {"status": 400, "body": "error: objective is not valid"}
        return MarketingManagement.get_all_optimization_goals_for_objective(objective)

# get all possible billing events for opt goal
@app.route("/api/fb/billing_events_for_opt_goal", methods=['GET'])
def fb_api_get_all_billing_events_for_opt_goal():
    if request.method == "GET":
        rq = request.get_json()
        optimization_goal = rq.get("optimization_goal")
        if (optimization_goal is None) or (optimization_goal == ""):
            return {"status": 400, "body": "error: optimization_goal cannot be null or empty string"}
        if optimization_goal not in MarketingManagement.all_possible_opt_goals:
            return {"status": 400, "body": "error: optimization_goal is not valid"}
        return MarketingManagement.get_all_possible_billing_events_for_opt_goal(optimization_goal)


# ************ BUSINESS MANAGEMENT ************
# *********************************************

# get all client Business Managers by OQ user id
@app.route("/api/fb/get_all_client_BMs_by_oq_user_id", methods=['GET'])
def fb_api_get_all_client_BMs_by_oq_user_id():
    if request.method == "GET":
        rq = request.get_json()
        oq_user_id = rq.get("oq_user_id")
        if (oq_user_id is None) or (oq_user_id == ""):
            return {"status": 400, "body": "error: oq_user_id cannot be null or empty string"}
        return MarketingManagement.get_all_client_BMs_by_oq_user_id(oq_user_id)

# get all client ad accounts by Business Manager id
@app.route("/api/fb/get_all_client_ad_accounts_by_BM_id", methods=['GET'])
def fb_api_get_all_client_ad_accounts_by_BM_id():
    if request.method == "GET":
        rq = request.get_json()
        BM_id = rq.get("BM_id")
        if (BM_id is None) or (BM_id == ""):
            return {"status": 400, "body": "error: BM_id cannot be null or empty string"}
        return MarketingManagement.get_all_client_ad_accounts_by_BM_id(BM_id)

# get all client pages by Business Manager id
@app.route("/api/fb/get_all_client_pages_by_BM_id", methods=['GET'])
def fb_api_get_all_client_pages_by_BM_id():
    if request.method == "GET":
        rq = request.get_json()
        BM_id = rq.get("BM_id")
        if (BM_id is None) or (BM_id == ""):
            return {"status": 400, "body": "error: BM_id cannot be null or empty string"}
        return MarketingManagement.get_all_client_pages_by_BM_id(BM_id)

# get all pixels for ad account
@app.route("/api/fb/get_all_ad_account_pixels", methods=['GET'])
def fb_api_get_all_ad_account_pixels():
    if request.method == "GET":
        rq = request.get_json()
        token = ''

        oq_user_id = rq.get('oq_user_id')
        BM_id = rq.get('BM_id')
        if (oq_user_id is not None) and (oq_user_id != "") and (BM_id is not None) and (BM_id != ""):
            token = MarketingManagement.get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id)
            if token == -1:
                return {"status": 400, "body": "error: OptimusQ userid or Client's Business Manager id not found"}

        ad_account = rq.get("ad_account")
        if (ad_account is None) or (ad_account == ""):
            return {"status": 400, "body": "error: ad_account cannot be null or empty string"}
        return MarketingManagement.get_all_ad_account_pixels(token, ad_account)


################################################# Google-Ads ##########################################################

# # todo add try and catch
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
#         # try:
#         #      campaign_id = res.get('body').get('id')
#         #      db.addCampaign(campaign_id, ad_account_id, campaign_name, objective, status)
#         #  except Exception as e:
#         #      print(str(e))
#         return res
#
#
# # get_all_campaigns
# @app.route("/api/GoogleAds/get_all_campaigns", methods=['GET'])
# def googleAds_api_get_all_campaigns():
#     if request.method == "GET":
#         rq = request.get_json(force=True)
#         customer_id = rq['customer_id']
#         return CampaignManagement.get_all_campaigns(customer_id)
#
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
#
# # create_new_ad_group
# @app.route("/api/GoogleAds/create_new_ad_group", methods=['POST'])
# def googleAds_api_create_new_ad_group():
#     if request.method == "POST":
#         rq = request.get_json(force=True)
#         customer_id = rq.get('customer_id')
#         campaign_id = rq.get('campaign_id')
#         name = rq.get('name')
#         cpc_bid = rq.get('cpc_bid')  # cost per click in IL shekels
#         status = rq.get('status', 'ENABLED')
#         res = CampaignManagement.create_new_adgroup(customer_id, campaign_id, name, status, cpc_bid)
#         # try:
#         #     adset_id = res.get('body').get('id')
#         #     db.addAdSet(adset_id, ad_account_id, campaign_id, ad_set_name, daily_budget, 'targeting')
#         # except Exception as e:
#         #     print(str(e))
#         return res
#
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
#         # try:
#         #     adset_id = res.get('body').get('id')
#         #     db.addAdSet(adset_id, ad_account_id, campaign_id, ad_set_name, daily_budget, 'targeting')
#         # except Exception as e:
#         #     print(str(e))
#         return res
#
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
#         res = CampaignManagement.create_new_responsive_search_ad(customer_id, ad_group_id, headlines_texts,
#                                                                  descriptions_texts, final_url, pinned_text)
#         # try:
#         #      campaign_id = res.get('body').get('id')
#         #      db.addCampaign(campaign_id, ad_account_id, campaign_name, objective, status)
#         #  except Exception as e:
#         #      print(str(e))
#         return res
#
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
# if __name__ == '__main__':
#     app.run()

# for running in local host with HTTPS
# first, create cert.pem and key.pem with the following cmd command:
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
# run with cmd command: python app.py
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
