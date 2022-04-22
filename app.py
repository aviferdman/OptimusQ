# This file is responsible for the UI.
# It is directly linked to any change we make in the business layer.
# That is, we can conveniently send a URL and see if what we expected to receive was received.

# 'Flask' is a library of web applications written in Python.
from flask import Flask, render_template, request, flash, Markup, jsonify

from DataBaseService.main import DataBaseController, dataBaseController
# deleteAccessTokenByUserId, writeAccessToken2db, getAccessTokenByUserId

from PresentationService.main import main_trigger

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"


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
        print("access_token: " + access_token)
        print("user_id: " + user_id)
        db = dataBaseController
        print("deleting from db...")
        db.deleteAccessTokenByUserId(user_id)
        # print("inserting to db...")
        # db.writeAccessToken2db(user_id, access_token)
        # print("db has tokens:")
        # return db.getAccessTokenByUserId(user_id)
    return "/fb_login_handler"


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


# for running in local host with HTTP
# if __name__ == '__main__':
#     app.run()

# for running in local host with HTTPS
# first, create cert.pem and key.pem with the following cmd command:
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
# run with cmd command: python app.py
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))