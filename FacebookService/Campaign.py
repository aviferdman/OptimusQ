import requests

# ************ Campaign MANAGEMENT ************
# *********************************************

# creates a new campaign.
# all params are string. special_ad_categories in the form: "[]"
# returns: new campaign's id
def create_new_campaign(access_token, ad_account_id, campaign_name, objective="LINK_CLICKS",
                        status="PAUSED", special_ad_categories="[]"):
    if "act_" not in ad_account_id:
        ad_account_id = "act_" + ad_account_id
    url = 'https://graph.facebook.com/v13.0/' + ad_account_id + '/campaigns'
    payload = {'name': campaign_name,
               'objective': objective,
               "status": status,
               'special_ad_categories': special_ad_categories,
               'access_token': access_token}
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns a campaign by id
def get_campaign_by_id(access_token, campaign_id):
    fields = 'fields=id,name,budget_remaining,daily_budget,objective'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + campaign_id + '/?' +
                       fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all campaign belongs to AD_ACCOUNT_ID
def get_all_campaigns(access_token, ad_account_id):
    fields = 'fields=campaigns{budget_remaining,can_create_brand_lift_study,configured_status,created_time,name,objective,special_ad_categories,start_time,status,updated_time}'
    params = {
        'access_token': access_token
    }
    res = requests.get(
        'https://graph.facebook.com/v13.0/act_' + ad_account_id + '?' + fields, params)
    if res.status_code != 200:
        return {"status": 400, "body": res.json()}
    myRes = {"status": res.status_code, "body": {"data": []}}
    if (res.json() is not None) and (res.json().get('campaigns') is not None) and (
            res.json().get('campaigns').get('data') is not None):
        myRes["body"]["data"] = res.json().get('campaigns').get('data')
    if (res.json() is not None) and (res.json().get('campaigns') is not None) and (
            res.json().get('campaigns').get('paging') is not None):
        myRes["body"]["paging"] = res.json().get('campaigns').get('paging')
    return myRes

# returns: success: bool
def delete_campaign(access_token, campaign_id):
    url = 'https://graph.facebook.com/v13.0/' + campaign_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}