import requests

# ************ Ad Creative MANAGEMENT ************
# *********************************************

# returns all ad creatives belongs to ad account
def get_all_ad_creatives(access_token, ad_account):
    fields = 'fields=id,name,title,body,image_hash'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/act_' + ad_account + '/adcreatives?' + fields, params)
    return {"status": res.status_code, "body": res.json()}

# creates a new ad creative
def create_ad_creative(access_token, name, image_hash, ad_account_id, link, message, page_id='107414948611212'):
    if "act_" not in ad_account_id:
        ad_account_id = "act_" + ad_account_id
    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "image_hash": image_hash,
            "link": link,
            "message": message
        }
    }
    url = 'https://graph.facebook.com/v13.0/' + ad_account_id + '/adcreatives'
    payload = {'name': name,
               'object_story_spec': str(object_story_spec),
               "access_token": access_token
               }
    res = requests.post(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}


# creates an ad of type "carousel"
# todo: make this function generic
def create_carousel_ad(access_token, name, image_hash, link, description, page_id='107414948611212'):
    object_story_spec = {
        "page_id": page_id,
        "link_data": {
            "child_attachments": [
                {
                    "description": description,
                    "image_hash": image_hash,
                    "link": link,
                    "name": "Product 1",
                    # "video_id": "<VIDEO_ID>"
                },
                {
                    "description": "$1.99",
                    "image_hash": image_hash,
                    "link": "https://www.ynet.co.il/",
                    "name": "Product 2",
                    # "video_id": "<VIDEO_ID>"
                }
            ],

            "link": "https://facebook.com/" + page_id,
        }
    }
    url = 'https://graph.facebook.com/v13.0/act_1394987677611796/adcreatives'
    payload = {'name': name,
               'object_story_spec': str(object_story_spec),
               "access_token": access_token
               }
    return requests.post(url, data=payload, headers={})

# returns: success: bool
def delete_ad_creative(access_token, ad_creative_id):
    url = 'https://graph.facebook.com/v13.0/' + ad_creative_id
    payload = {"access_token": access_token}
    res = requests.delete(url, data=payload, headers={})
    return {"status": res.status_code, "body": res.json()}