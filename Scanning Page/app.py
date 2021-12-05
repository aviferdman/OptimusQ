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
		abort(404, message="url is incorrect")
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
		abort(404, message="url is incorrect")
	res_json = {"title": result.text}
	return res_json


@app.route('/extract_keywords', methods=['POST', 'GET'])
def extract_keywords():
	reco = recoSystem.RecoSystem()
	url = request.args.get('url')
	result = reco.extract_keywords_from_landing_page(url)
	if not result:
		abort(404, message="url is incorrect")
	res_json = {"keywords": result}
	return res_json


if __name__ == '__main__':
	app.run()



