import MarketingManagement

# represents a Business
from AdAccount import AdAccount
from Response import Response


class Business:
    def __init__(self, id):
        self.id = id
        self.adAccounts = {}  # key: ad account id. value: ad account

    # returns ok Response if succeed
    def delete_ad_account(self, access_token, business_id, ad_account_id):
        res = MarketingManagement.delete_ad_account(access_token, business_id, ad_account_id)
        if res.status_code == 200:
            self.adAccounts.pop(ad_account_id) # todo: change to ad account id
            return Response(True, "", res.status_code, res.text)
        else:
            return Response(False, res.text, res.status_code, "")

    # returns ok Response if succeed
    def delete_campaign(self, access_token, ad_account_id, campaign_id):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found", -1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.delete_campaign(self, access_token, campaign_id)

    # returns ok Response if succeed
    def delete_adSet(self, access_token, ad_account_id, campaign_id, adSet_id):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found", -1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.delete_adSet(self, access_token, campaign_id, adSet_id)

    # returns ok Response if succeed
    def delete_ad_creative(self, access_token, ad_account_id, ad_creative_id):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found", -1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.delete_ad_creative(self, access_token, ad_creative_id)

    # returns ok Response if succeed
    def delete_ad(self, access_token, ad_account_id, campaign_id, adSet_id, ad_id):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found", -1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.delete_ad(self, access_token, campaign_id, adSet_id, ad_id)

    def create_ad_account(self, account_name, access_token, currency, timezone_id,
                                   end_advertiser, media_agency, partner):
        res = MarketingManagement.create_ad_account(self.id, account_name, access_token, currency, timezone_id,
                                   end_advertiser, media_agency, partner)
        if res.status_code == 200:
            self.adAccounts.update(AdAccount(res.text)) # todo: change to ad account id
            return Response(True, "", res.status_code, res.text)
        else:
            return Response(False, res.text, res.status_code, "")

    def get_ad_account_by_id(self, ad_account_id, access_token):
        if ad_account_id not in self.adAccounts:
            return Response(False, "ad account id not found", -1, "")
        return Response(True, "", 0, "", self.adAccounts[ad_account_id])

    def get_all_ad_accounts(self, access_token):
        return Response(True, "", 0, "", self.adAccounts.values())

    def create_new_campaign(self, ad_account_id, access_token, campaign_name, objective,
                            status, special_ad_categories):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",-1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.create_new_campaign(self, access_token, campaign_name, objective,
                        status, special_ad_categories)


    def get_campaign_by_id(self, ad_account_id, access_token, campaign_id):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",
                                -1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.get_campaign_by_id(access_token, campaign_id)

    def get_all_campaigns(self, ad_account_id, access_token):
        if ad_account_id not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",
                                -1, "")
            return response
        ad_account = self.adAccounts[ad_account_id]
        return ad_account.get_all_campaigns(access_token)

    def create_new_ad_set(self, AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status):
        if AD_ACCOUNT_ID not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",
                                -1, "")
            return response
        ad_account = self.adAccounts[AD_ACCOUNT_ID]
        return ad_account.create_new_ad_set(AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status)

    # adds an image to ad creative repository.
    # image_path - path of image to upload, from local computer.
    # returns image's hash
    # todo: save image in database
    def upload_image(self, AD_ACCOUNT_ID, access_token, image_path):
        if AD_ACCOUNT_ID not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",
                                -1, "")
            return response
        ad_account = self.adAccounts[AD_ACCOUNT_ID]
        return ad_account.upload_image(AD_ACCOUNT_ID, access_token, image_path)

    # creates a new ad creative
    # todo: returns error: "Ads creative post was created by an app that is in development mode. It must be in public to create this ad"
    # todo: make this function generic
    def create_ad_creative(self, AD_ACCOUNT_ID, name, access_token, image_hash):
        if AD_ACCOUNT_ID not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",
                                -1, "")
            return response
        ad_account = self.adAccounts[AD_ACCOUNT_ID]
        return ad_account.create_ad_creative(name, access_token, image_hash)


    # creates a new ad
    def create_ad(self, campaign_id, ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status):
        if AD_ACCOUNT_ID not in self.adAccounts.keys():
            response = Response(False, "ad account id not found",
                                -1, "")
            return response
        ad_account = self.adAccounts[AD_ACCOUNT_ID]
        return ad_account.create_ad(campaign_id, ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status)