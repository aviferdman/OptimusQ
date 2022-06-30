import requests

# ************ Ad Account MANAGEMENT ************
# *********************************************

# create a new ad account
# for free business account, there's a limit for only 1 ad account!
def create_ad_account(access_token, business_id, account_name, currency, timezone_id,
                      end_advertiser='NONE', media_agency='NONE', partner='NONE'):
    url = 'https://graph.facebook.com/v13.0/' + business_id + '/adaccount'
    payload = {'name': account_name,
               'currency': currency,
               "timezone_id": timezone_id,
               'end_advertiser': end_advertiser,
               'media_agency': media_agency,
               'partner': partner,
               'access_token': access_token}
    return requests.post(url, data=payload, headers={})


# get ad account by id
def get_ad_account_by_id(access_token, ad_account_id):
    fields = 'fields=account_id,name,account_status,amount_spent,currency,owner,timezone_name,campaigns{id,name}'
    params = {
        'access_token': access_token
    }
    return requests.get('https://graph.facebook.com/v13.0/act_' + ad_account_id + '/?' +
                        fields, params)


# returns all ad accounts belong to business_id
def get_all_ad_accounts_in_business(access_token, business_id):
    fields = 'fields=owned_ad_accounts{name,account_id}'
    params = {'access_token': access_token}
    res = requests.get('https://graph.facebook.com/v13.0/' + business_id + '?' + fields, params)
    return res

# You cannot remove ad accounts from your business if you're OWNER and if the accounts are CONFIRMED.
# If you have a PENDING access request or you have AGENCY access to the ad account, you can make this DELETE call
def delete_ad_account(access_token, business_id, ad_account_id):
    url = 'https://graph.facebook.com/v13.0/' + business_id + '/ad_accounts'
    payload = {'adaccount_id': ad_account_id,
               "access_token": access_token
               }
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}