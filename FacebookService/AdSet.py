import requests

# ************ Ad Set MANAGEMENT ************
# *********************************************

# creates a new ad set
def create_new_ad_set(access_token, AD_ACCOUNT_ID, ad_set_name, campaign_id, daily_budget="1000",
                      optimization_goal='REACH',
                      billing_event='IMPRESSIONS', bid_amount="1500",
                      start_time='1633851746', status='PAUSED',
                      targeting_min_age='NONE', targeting_max_age='NONE', targeting_countries=["IL"], end_time='NONE',
                      targeting_gender="NONE", targeting_relationship_statuses="NONE",
                      targeting_interests=[], targeting_behaviors=[], promoted_object=None):
    if "act_" not in AD_ACCOUNT_ID:
        AD_ACCOUNT_ID = "act_" + AD_ACCOUNT_ID
    url = 'https://graph.facebook.com/v13.0/' + AD_ACCOUNT_ID + '/adsets'
    targeting = {}
    if targeting_min_age != 'NONE':
        targeting["age_min"] = targeting_min_age
    if targeting_max_age != 'NONE':
        targeting["age_max"] = targeting_max_age
    targeting["geo_locations"] = {"countries": targeting_countries}
    if targeting_gender != "NONE":
        tmp_lst = list()
        tmp_lst.append(targeting_gender)
        targeting["genders"] = tmp_lst
    if targeting_relationship_statuses != "NONE":
        targeting["relationship_statuses"] = targeting_relationship_statuses
    if len(targeting_interests) > 0:
        targeting["interests"] = targeting_interests
    if len(targeting_behaviors) > 0:
        targeting["behaviors"] = targeting_behaviors

    payload = {'name': ad_set_name,
               'optimization_goal': optimization_goal,
               "billing_event": billing_event,
               "bid_amount": bid_amount,
               "daily_budget": daily_budget,
               "campaign_id": campaign_id,
               "targeting": str(targeting),
               "start_time": start_time,
               "status": status,
               "access_token": access_token
               }
    if promoted_object is not None:
        payload["promoted_object"] = str(promoted_object)

    if end_time != 'NONE':
        payload["end_time"] = end_time
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# returns all ad sets belongs to AD_ACCOUNT_ID
def get_all_ad_sets_by_ad_account(access_token, ad_account_id, with_status="['ACTIVE', 'PAUSED']"):
    fields = 'fields=daily_budget,name,targeting,created_time,billing_event,start_time,end_time,optimization_goal,status,updated_time'
    params = {
        'access_token': access_token
    }
    if with_status != "['ACTIVE', 'PAUSED']":
        params['effective_status'] = with_status
    res = requests.get('https://graph.facebook.com/v13.0/act_' + ad_account_id + '/adsets?' + fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all ad sets belongs to campaign with campaign_id
def get_all_ad_sets_by_campaign(access_token, campaign_id):
    fields = 'fields=daily_budget,name,targeting,created_time,billing_event,start_time,end_time,optimization_goal,status,updated_time,campaign_id,promoted_object,bid_amount'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + campaign_id + '/adsets?' + fields, params)
    if res.status_code != 200:
        return {"status": res.status_code, "body": res.json()}
    myRes = {"status": res.status_code, "body": {"data": []}}
    if res.json().get("paging", None) is not None:
        myRes["body"]["paging"] = res.json().get("paging")
    res_list = list()
    if (res.json() is not None) and (res.json().get('data') is not None):
        for adset in res.json().get('data'):
            if adset.get("targeting", None) is None:
                res_list.append(adset)
                continue
            adset["targeting_min_age"] = adset.get("targeting").get("age_min", None)
            adset["targeting_max_age"] = adset.get("targeting").get("age_max", None)
            targeting_countries_str = ''
            if (adset.get("targeting").get("geo_locations", None) is not None) and (
                    adset.get("targeting").get("geo_locations").get("countries") is not None):
                for country in adset.get("targeting").get("geo_locations").get("countries"):
                    targeting_countries_str += country + ','
            if len(targeting_countries_str) == 0:
                targeting_countries_str = None
            adset["targeting_countries"] = targeting_countries_str
            adset["targeting_interests"] = adset.get("targeting").get("interests", None)
            adset["targeting_behaviors"] = adset.get("targeting").get("behaviors", None)
            if adset.get("targeting").get("genders", None) is not None:
                if len(adset.get("targeting").get("genders")) == 0:
                    adset["targeting_gender"] = None
                else:
                    if (1 in adset.get("targeting").get("genders")) or ('1' in adset.get("targeting").get("genders")):
                        adset["targeting_gender"] = 1
                    else:
                        adset["targeting_gender"] = 2

            targeting_relationship_statuses_str = ''
            if adset.get("targeting").get("relationship_statuses", None) is not None:
                for status in adset.get("targeting").get("relationship_statuses"):
                    targeting_relationship_statuses_str += str(status) + ','
            if len(targeting_relationship_statuses_str) == 0:
                targeting_relationship_statuses_str = None
            adset["targeting_relationship_statuses"] = targeting_relationship_statuses_str
            adset.pop('targeting', None)  # delete targeting for formatting the json
            res_list.append(adset)
    myRes["body"]["data"] = res_list
    return myRes

# returns: success: bool
def delete_adSet(access_token, adSet_id):
    url = 'https://graph.facebook.com/v13.0/' + adSet_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}