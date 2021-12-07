import recoSystem


def extract_title(url):
	reco = recoSystem.RecoSystem()
	x, result = reco.scan_landing_page(url)
	if not result:
		return ["Can't extract the data from this url... working on it:)"]
	return result


def extract_keywords(url):
	reco = recoSystem.RecoSystem()
	result = reco.extract_keywords_from_landing_page(url)
	if len(result) == 0:
		return ["Can't extract the data from this url... working on it:)"]
	return result


if __name__ == '__main__':
	print("Hello World")


