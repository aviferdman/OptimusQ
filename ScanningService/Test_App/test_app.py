from flask import Flask, render_template, request, flash, abort, Markup

# import recoSystem
from ScanningService import recoSystem
# from recoSystem import RecoSystem

app = Flask(__name__)

app.secret_key = "manbearpig_MUDMAN888"


@app.route("/")
def hello():
    # return "Hello, World!"
    return render_template("main_index.html")

@app.route("/extract_data", methods=['POST', 'GET'])
def extract_keywords_from_landing_page():
    url = str(request.form['url'])
    reco = recoSystem.RecoSystem()
    result = reco.scrap_page(url)
    if not result:
        flash("Can't extract the data from this url... working on it:)")
        return render_template("main_index.html")
    res_txt = "<b>Title: </b><br>"
    res_txt += result["title"]
    res_txt += "<br>"
    res_txt += "<br><b>Description:</b><br>"
    res_txt += result["description"]
    res_txt += "<br><br><b>Keywords:</b><br>"
    for kw in result["keywords"]:
        res_txt += kw + "<br>"
    flash(Markup(res_txt))
    return render_template("main_index.html" ) #, output=list_of_images)


# check2
if __name__ == '__main__':
    app.run()
    # reco = recoSystem.RecoSystem()
    # url = "https://www.bloomberg.com/press-releases/2021-12-20/authoritytech-llc-authoritytech-i[…]stars-backed-optimusq-to-unveil-ai-powered-hybrid-pr-service"
    # result = reco.scrap_page(url)
    # result = main_trigger(url)
    # print(result)


# import recoSystem
# from flask import Flask, render_template, request, flash, abort, Markup

# app = Flask(__name__)
# app.secret_key = "manbearpig_MUDMAN888"


# @app.route("/")
# def index():
#     return render_template("main_index.html")
