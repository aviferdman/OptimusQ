# This file is responsible for the UI.
# It is directly linked to any change we make in the business layer.
# That is, we can conveniently send a URL and see if what we expected to receive was received.

# 'Flask' is a library of web applications written in Python.
from doctest import OutputChecker
from flask import Flask, render_template, request, flash, Markup, jsonify
import time

from DataBaseService.main import DataBaseController, dataBaseController
# deleteAccessTokenByUserId, writeAccessToken2db, getAccessTokenByUserId

from FacebookService import MarketingManagement

from PresentationService.main import main_trigger

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

db = dataBaseController


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
    if request.method == "POST":
        print("POST!!!: ")
        rq = request.get_json()
        user_id = rq["user_id"]
        access_token = rq["access_token"]
        print("user_id: " + user_id)

        ad_accounts = [] + MarketingManagement.get_all_ad_accounts_in_business(access_token).json()['data']
        campaigns = []
        ad_sets = []
        for account in ad_accounts:
            # ad_account_id = account['id'][4::] # only the id, without the prefix of act_
            ad_account_id = account['account_id']
            campaigns = campaigns + (MarketingManagement.get_all_campaigns(ad_account_id, access_token).json()["campaigns"]["data"])
            ad_sets = ad_sets + (MarketingManagement.get_all_ad_sets_by_ad_account(access_token, ad_account_id).json()['data'])
        ads = []
        for ad_set in ad_sets:
            ad_set_id = ad_set['id']
            print("ad_set: " + str(ad_set_id))
            ads = ads + (MarketingManagement.get_all_ads_by_adSet_id(access_token, ad_set_id).json()['data'])
    #     todo: to get ad creatives: An ad creative object is an instance of a specific creative which is being used to define the creative field of one or more ads


    #     db = dataBaseController
        # print("deleting from db...")
        # db.deleteAccessTokenByUserId(user_id)
        # print("inserting to db...")
        # db.writeAccessToken2db(user_id, access_token)
        # print("db has tokens:")
        # return db.getAccessTokenByUserId(user_id)
    # return "/fb_login_handler"
    # output_json = {}
    # output_json.update("campaigns")
    list_of_images = []
    list_of_images.append("1")
    list_of_images.append("2")
    return render_template("fb_logged_in.html", output={"ad_accounts": ad_accounts, "campaigns": campaigns, "ad_sets": ad_sets, "ads": ads})
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
        url = rq["url"] #image url
        daily_budget = rq["daily_budget"]
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
        print("**DEBUG2")
        print("**response from FB: " + str(MarketingManagement.upload_image_by_url(ad_account, access_token, url).json()))

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
    return render_template("create_adset_handler.html", output2=ad_accounts)


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

@app.route("/api/fb/upload_img_from_url", methods=['POST'])
def upload_img_from_url():
    if request.method == "POST":
        print("upload_img_from_url: POST!")
        rq = request.get_json()
        ad_account_id = rq['ad_account']
        img_url = rq['img_url']
        token = db.getAccessTokenByUserId('admin_token')
        # MarketingManagement.upload_image_by_url('1394987677611796', token, 'https://artprojectsforkids.org/wp-content/uploads/2020/05/Airplane.jpg')
        MarketingManagement.upload_image_by_url(ad_account_id, token, img_url)
        return "success"


# for running in local host with HTTP
# if __name__ == '__main__':
#     app.run()

# for running in local host with HTTPS
# first, create cert.pem and key.pem with the following cmd command:
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
# run with cmd command: python app.py
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
