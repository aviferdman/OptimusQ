from flask import Flask, render_template, request, flash, abort, Markup
import recoSystem

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/extract_data", methods=['POST', 'GET'])
def extract_keywords_from_landing_page():
	reco = recoSystem.RecoSystem()
	url = str(request.form['name_input'])
	result = reco.extract_keywords_from_landing_page(url)
	x, res_title = reco.scan_landing_page(url)
	if not result:
		flash("Can't extract the data from this url... working on it:)")
		return render_template("index.html")
	res_txt = "<b>Title: </b>"
	res_txt += str(res_title.text)
	res_txt += "<br>"
	res_txt += "<br><b>Keywords:</b><br>"
	for r in result:
		res_txt += str(r) + "<br>"
	flash(Markup(res_txt))
	return render_template("index.html")

@app.route('/extract_title', methods=['POST', 'GET'])
def extract_title_from_landing_page():
	reco = recoSystem.RecoSystem()
	url = request.args.get('url')
	x, result = reco.scan_landing_page(url)
	if not result:
		return {"message": "Can't extract the data from this url... working on it:)"}
	res_json = {"title": result.text}
	return res_json

@app.route('/extract_keywords', methods=['POST', 'GET'])
def extract_keywords():
	reco = recoSystem.RecoSystem()
	url = request.args.get('url')
	result = reco.extract_keywords_from_landing_page(url)
	if len(result) == 0:
		return {"message": "Can't extract the data from this url... working on it:)"}
	res_json = {"keywords": result}
	return res_json



if __name__ == '__main__':
	app.run()
	# reco = recoSystem.RecoSystem()
	# url = "https://www.sonoviastore.co.il/blogs/news/%D7%94%D7%9E%D7%A1%D7%9B%D7%94-%D7%94%D7%98%D7%95%D7%91%D7%94-%D7%91%D7%99%D7%95%D7%AA%D7%A8-%D7%9C%D7%98%D7%99%D7%A1%D7%95%D7%AA-%D7%91%D7%A9%D7%A0%D7%AA-2021-%D7%A1%D7%95%D7%A0%D7%95%D7%91%D7%99%D7%94?utm_source=taboola&utm_medium=referral&utm_campaign=TB_Blog_AirTravel_IL_PC&tblci=GiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyDq3U8oxaqc6ZT4jY_QAQ#tblciGiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyDq3U8oxaqc6ZT4jY_QAQ"
	# result = reco.extract_keywords_from_landing_page(url)
	# print(result)


