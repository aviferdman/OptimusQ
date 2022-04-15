# represents a BusinessController
from Response import Response


class BusinessController:
    def __init__(self, id):
        self.id = id
        self.businesses = {}  # key: business id. value: business

    # You cannot remove ad accounts from your business if you're OWNER and if the accounts are CONFIRMED.
    # If you have a PENDING access request or you have AGENCY access to the ad account, you can make this DELETE call
    def delete_ad_account(self, access_token, business_id, ad_account_id):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.delete_ad_account(access_token, business_id, ad_account_id)

    def delete_campaign(self, access_token, business_id, ad_account_id, campaign_id):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.delete_campaign(access_token, ad_account_id, campaign_id)

    def delete_adSet(self, access_token, business_id, ad_account_id, campaign_id, adSet_id):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.delete_adSet(access_token, ad_account_id, campaign_id, adSet_id)

    def delete_ad_creative(self, access_token, business_id, ad_account_id, ad_creative_id):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.delete_ad_creative(access_token, ad_account_id, ad_creative_id)

    def delete_ad(self, access_token, business_id, ad_account_id, campaign_id, adSet_id, ad_id):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.delete_ad(access_token, ad_account_id, campaign_id, adSet_id, ad_id)

    def create_ad_account(self, business_id, account_name, access_token, currency, timezone_id,
                          end_advertiser='NONE', media_agency='NONE', partner='NONE'):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.create_ad_account(business_id, account_name, access_token, currency, timezone_id,
                                   end_advertiser, media_agency, partner)

    def get_ad_account_by_id(self, business_id, ad_account_id, access_token):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.get_ad_account_by_id(ad_account_id, access_token)

    def get_all_ad_accounts(self, business_id, access_token):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.get_all_ad_accounts(access_token)

    def get_campaign_by_id(self, business_id, ad_account_id, access_token, campaign_id):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.get_campaign_by_id(ad_account_id, access_token, campaign_id)

    def get_all_campaigns(self, business_id, ad_account_id, access_token):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.get_all_campaigns(ad_account_id, access_token)

    def create_new_ad_set(self, business_id, AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.create_new_ad_set(AD_ACCOUNT_ID, ad_set_name, access_token, campaign_id, optimization_goal,
                          billing_event, bid_amount, daily_budget,
                          targeting,
                          start_time, status)

    # adds an image to ad creative repository.
    # image_path - path of image to upload, from local computer.
    # returns image's hash
    # todo: save image in database
    def upload_image(self, business_id, AD_ACCOUNT_ID, access_token, image_path):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.upload_image(AD_ACCOUNT_ID, access_token, image_path)

    # creates a new ad creative
    # todo: returns error: "Ads creative post was created by an app that is in development mode. It must be in public to create this ad"
    # todo: make this function generic
    def create_ad_creative(self, business_id, AD_ACCOUNT_ID, name, access_token, image_hash):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.create_ad_creative(name, access_token, image_hash)


    # creates a new ad
    def create_ad(self, business_id, campaign_id, ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status):
        if business_id not in self.businesses.keys():
            response = Response(False, "business id not found",
                                -1, "")
            return response
        business = self.businesses[business_id]
        return business.create_ad(campaign_id, ad_set_id, access_token, AD_ACCOUNT_ID, name, adset_id, creative_id, status)