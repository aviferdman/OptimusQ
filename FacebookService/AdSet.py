import MarketingManagement

# represents an Ad Set
from Ad import Ad
from Response import Response


class AdSet:
    def __init__(self, id):
        self.id = id
        self.ads = {}  # key: ad id. value: ad

    # creates a new ad
    def create_ad(self, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status):
        res = MarketingManagement.create_ad(access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status)
        if res.status_code == 200:
            id = res.text  # todo: maybe id is substring?
            self.ads.update(Ad(id))
            return Response(True, "", res.status_code, res.text, self.ads[id])
        else:
            return Response(False, res.text, res.status_code, "")