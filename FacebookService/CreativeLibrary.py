import MarketingManagement

# represents a Creative Library
from AdCreative import AdCreative
from Response import Response


class CreativeLibrary:
    def __init__(self):
        # self.id = id
        self.ad_creatives = {}  # key: ad_creative id. value: ad_creative

    # creates a new ad creative
    # todo: returns error: "Ads creative post was created by an app that is in development mode. It must be in public to create this ad"
    # todo: make this function generic
    def create_ad_creative(self, name, access_token, image_hash):
        res = MarketingManagement.create_ad_creative(name, access_token, image_hash)
        if res.status_code == 200:
            id = res.text  # todo: maybe id is substring?
            self.ad_creatives.append(AdCreative(id))
            return Response(True, "", res.status_code, res.text, self.ad_creatives[id])
        else:
            return Response(False, res.text, res.status_code, "")