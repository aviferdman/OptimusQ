import requests

# ************ Pixel MANAGEMENT ************
# *********************************************

# returns all pixels ids for business
def get_all_business_pixels(access_token, business_id):
    fields = 'fields=owned_pixels{id,name}'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/' + business_id + '?' + fields, params)


# returns all pixels for ad account
def get_all_ad_account_pixels(access_token, ad_account_id):
    if "act_" not in ad_account_id:
        ad_account_id = "act_" + ad_account_id
    fields = 'fields=adspixels{id,name}'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + ad_account_id + '?' + fields, params)
    if (res.json() is not None) and (res.json().get('adspixels') is not None) and (
            res.json().get('adspixels').get('data') is not None):
        return {"status": res.status_code, "body": {"data": res.json().get('adspixels').get('data')}}
    return {"status": res.status_code, "body": {"data": []}}