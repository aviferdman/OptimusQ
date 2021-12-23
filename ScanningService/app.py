from flask import Flask, render_template, request, flash, abort, Markup

import recoSystem
from main import main_trigger
from recoSystem import RecoSystem

app = Flask(__name__)

app.secret_key = "manbearpig_MUDMAN888"


@app.route("/")
def hello():
    # return "Hello, World!"
    return render_template("index.html")

@app.route("/extract_data", methods=['POST', 'GET'])
def extract_keywords_from_landing_page():
    url = str(request.form['url'])
    result =main_trigger(url)
    if not result:
        flash("Can't extract the data from this url... working on it:)")
        return render_template("index.html")
    images = result["images"]
    list_of_images = []
    for k in result["keywords"]:
        if images[k]: #todo???
         list_of_images.append(images[k][0])
    # if len(result) == 0:
    #     return func.HttpResponse("Can't extract the data from this url... working on it:)")
    res_txt = "<b>Title: </b><br>"
    res_txt += result["title"]
    res_txt += "<br>"
    res_txt += "<br><b>Description:</b><br>"
    res_txt += result["description"]
    res_txt += "<br><br><b>Keywords:</b><br>"
    for kw in result["keywords"]:
        res_txt += kw + "<br>"
    res_txt += "<br><b>Recommended Images:</b>"
    flash(Markup(res_txt))
    return render_template("index.html", output=list_of_images)


# check2
if __name__ == '__main__':
    app.run()
    # reco = recoSystem.RecoSystem()
    # url = "https://finance.yahoo.com/news/meatech-3d-reports-breakthrough-cultured-130000799.htm[…]MeaTech+-+Group+3+-+Wide+-+Mobile+-+8%2F12%2F21&guccounter=1"
    # result = reco.scrap_page(url)
    # # result = main_trigger(url)
    # print(result)


# import recoSystem
# from flask import Flask, render_template, request, flash, abort, Markup

# app = Flask(__name__)
# app.secret_key = "manbearpig_MUDMAN888"


# @app.route("/")
# def index():
#     return render_template("index.html")
