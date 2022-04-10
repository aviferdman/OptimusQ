import MarketingManagement

# represents a Campaign
from AdSet import AdSet
from Response import Response


class Campaign:
    def __init__(self, id):
        self.id = id
        self.campaign_statistics = {}  # key: statistics id. value: campaign statistics
        self.ad_sets = {}   # key: ad set id. value: ad set

    # creates a new ad set
    def create_new_ad_set(self, AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status):
        res = MarketingManagement.create_new_ad_set(AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status)
        if res.status_code == 200:
            id = res.text   # todo: maybe id is substring?
            self.ad_sets.update(AdSet(id))
            return Response(True, "", res.status_code, res.text, self.ad_sets[id])
        else:
            return Response(False, res.text, res.status_code, "")


    # creates a new ad
    def create_ad(self, ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status):
        if ad_set_id not in self.ad_sets.keys():
            response = Response(False, "ad set id not found",
                                -1, "")
            return response
        ad_set = self.ad_sets[ad_set_id]
        return ad_set.create_ad(access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status)