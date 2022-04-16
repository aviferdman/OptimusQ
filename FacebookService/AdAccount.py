import MarketingManagement

# represents an Ad Account
from Campaign import Campaign
from CreativeLibrary import CreativeLibrary
from Response import Response


class AdAccount:
    def __init__(self, id):
        self.id = id
        self.creative_library = CreativeLibrary()
        self.campaigns = {} # key: campaign id. value: campaign

    def delete_campaign(self, access_token, campaign_id):
        if campaign_id not in self.campaigns.keys():
            return Response(False, "campaign id not found", -1, "")
        res = MarketingManagement.delete_campaign(access_token, campaign_id)
        if res.status_code == 200:
            self.campaigns.pop(campaign_id) # todo: change to ad account id
            return Response(True, "", res.status_code, res.text)
        else:
            return Response(False, res.text, res.status_code, "")

    def delete_ad_creative(self, access_token, ad_creative_id):
        if ad_creative_id not in self.creative_library.ad_creatives.keys():
            return Response(False, "ad creative id not found", -1, "")
        res = MarketingManagement.delete_ad_creative(access_token, ad_creative_id)
        if res.status_code == 200:
            self.creative_library.ad_creatives.pop(ad_creative_id)
            return Response(True, "", res.status_code, res.text)
        else:
            return Response(False, res.text, res.status_code, "")

    def delete_adSet(self, access_token, campaign_id, adSet_id):
        if campaign_id not in self.campaigns.keys():
            return Response(False, "campaign id not found", -1, "")
        campaign = self.campaigns[campaign_id]
        return campaign.delete_adSet(access_token, adSet_id)

    def delete_ad(self, access_token, campaign_id, adSet_id, ad_id):
        if campaign_id not in self.campaigns.keys():
            return Response(False, "campaign id not found", -1, "")
        campaign = self.campaigns[campaign_id]
        return campaign.delete_ad(access_token, adSet_id, ad_id)

    def create_new_campaign(self, access_token, campaign_name, objective,
                        status, special_ad_categories):
        res = MarketingManagement.create_new_campaign(self.id, access_token, campaign_name, objective,
                        status, special_ad_categories)
        if res.status_code == 200:
            self.campaigns.update(Campaign(res.text)) # todo: maybe id is substring?
            return Response(True, "", res.status_code, res.text)
        else:
            return Response(False, res.text, res.status_code, "")

    def get_campaign_by_id(self, access_token, campaign_id):
        if campaign_id not in self.campaigns.keys():
            response = Response(False, "campaign id not found", -1, "")
            return response
        return Response(True, "", 0, "", self.campaigns[campaign_id])

    def get_all_campaigns(self, access_token):
        return Response(True, "", 0, "", self.campaigns)


    def create_new_ad_set(self, AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget, targeting, start_time, status):
        if campaign_id not in self.campaigns.keys():
            return Response(False, "campaign id not found", -1, "")
        campaign = self.campaigns[campaign_id]
        return campaign.create_new_ad_set(AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status)

    # adds an image to ad creative repository.
    # image_path - path of image to upload, from local computer.
    # returns image's hash
    # todo: save image in database
    def upload_image(self, AD_ACCOUNT_ID, access_token, image_path):
        res = MarketingManagement.upload_image(AD_ACCOUNT_ID, access_token, image_path)
        if res.status_code == 200:
            return Response(True, "", res.status_code, res.text)
        else:
            return Response(False, res.text, res.status_code, "")


    # creates a new ad creative
    # todo: returns error: "Ads creative post was created by an app that is in development mode. It must be in public to create this ad"
    # todo: make this function generic
    def create_ad_creative(self, name, access_token, image_hash):
        return self.creative_library.create_ad_creative(name, access_token, image_hash)


    # creates a new ad
    def create_ad(self, campaign_id, ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status):
        if campaign_id not in self.campaigns.keys():
            response = Response(False, "campaign id not found", -1, "")
            return response
        campaign = self.campaigns[campaign_id]
        return campaign.create_ad(ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status)