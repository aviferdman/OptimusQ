import requests

# ************ Insights ************
# *********************************************

# get insights for ad account/campaign/ad set/ ad
def get_insights(access_token, marketing_object_id, date_preset='maximum'):
    url = 'https://graph.facebook.com/v13.0/' + marketing_object_id + '/insights'
    params = {'fields': 'impressions,clicks,cpc,ctr,frequency,objective,optimization_goal,quality_ranking,spend',
              'date_preset': date_preset,
              "access_token": access_token
              }
    res = requests.get(url, params)
    return {"status": res.status_code, "body": res.json()}