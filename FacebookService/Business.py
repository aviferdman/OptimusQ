import requests
from DataBaseService.main import dataBaseController

# ************ Business MANAGEMENT ************
# *********************************************
from FacebookService import Pixel

db = dataBaseController
business_id = 775308013448374  # OQ business id
OQ_app_id = 331878552252931

# returns all client BusinessManagers by oq_user_id
def get_all_client_BMs_by_oq_user_id(oq_user_id):
    res_BMs = list()
    try:
        for BM_record in db.getFB_CLIENT_BM_IDS_BY_OQ_USER_ID(oq_user_id):
            res_BMs.append(BM_record[1])
        return {"status": 200, "body": {"data": res_BMs}}
    except Exception as e:
        return {"status": 400, "body": str(e)}

# returns all client ad accounts by BM_id
def get_all_client_ad_accounts_by_BM_id(BM_id):
    ad_accounts_ids = list()
    try:
        for record in db.getFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(BM_id):
            ad_accounts_ids.append(record[1])
        return {"status": 200, "body": {"data": ad_accounts_ids}}
    except Exception as e:
        return {"status": 400, "body": str(e)}

# returns all client pages by BM_id
def get_all_client_pages_by_BM_id(BM_id):
    pages_ids = list()
    try:
        for record in db.getFB_CLIENT_PAGES_BY_BM_ID(BM_id):
            pages_ids.append(record[1])
        return {"status": 200, "body": {"data": pages_ids}}
    except Exception as e:
        return {"status": 400, "body": str(e)}


# get token for client by oq user id
def get_token_for_client_by_oq_user_id_and_business_id(oq_user_id, BM_id):
    try:
        return db.getFB_CLIENT_TOKEN_BY_OQ_USER_ID_AND_BM_ID(oq_user_id, BM_id)[0][4]
    except Exception as e:
        return -1


# returns all businesses by user id: id and name
def get_all_businesses_by_user_id(access_token, user_id):
    fields = 'fields=businesses{id,name}'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v14.0/' + user_id + '?' + fields, params)
    return {"status": res.status_code, "body": res.json()}


# returns all business asset groups
def get_all_business_asset_groups(access_token, business_id):
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + business_id + '/business_asset_groups', params)
    return {"status": res.status_code, "body": res.json()}


# returns all ASSETS_IDS for a business, for use in function create_on_behalf_of_relationship
def get_all_business_assets(access_token, business_id):
    fields = 'fields=owned_ad_accounts{name},owned_pages{name}'
    params = {
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/' + business_id + '?' + fields, params)
    return {"status": res.status_code, "body": res.json()}

# Create the On Behalf Of relationship between the partner and client's Business Manager.
# access token must be the user's and received by FB login - and not the app token.
# API tutorial for this function:
# https://developers.facebook.com/docs/marketing-api/business-manager/guides/on-behalf-of
# ASSETS_IDS is a list, containing assets ids for assigning from client BM to partner BM
def create_on_behalf_of_relationship(client_admin_access_token, client_user_id, oq_user_id):
    PARTNER_BM_ID = business_id  # OQ business id
    res = get_all_businesses_by_user_id(client_admin_access_token, client_user_id)
    if res.get('status') != 200:
        return res
    BMs_id_list = list()

    BMs_in_DB = list()
    for BM_record in db.getFB_CLIENT_BM_IDS_BY_OQ_USER_ID(oq_user_id):
        BMs_in_DB.append(BM_record[1])

    for BM in res.get('body').get('businesses').get('data'):  # get all businesses belong to user
        if BM.get('id') == str(PARTNER_BM_ID):
            continue
        BMs_id_list.append(BM.get('id'))
    # CLIENT_BM_ID = res.get('body').get('data')[1].get('id') # todo: allow client user to choose client BM id.

    succeeded_BMs_id_list = ""

    for CLIENT_BM_ID in BMs_id_list:
        # *** GET ALL BUSINESS ASSETS ***
        ASSETS_IDS = list()  # todo: allow client user to choose assets that belong to his business.
        res = get_all_business_assets(client_admin_access_token, CLIENT_BM_ID)
        if res.get('status') != 200:
            return res
        owned_ad_accounts_ids = list()
        if (res.get('body') is None) or (res.get('body').get('owned_ad_accounts') is None) or (
                res.get('body').get('owned_ad_accounts').get('data') is None):
            continue

        for ad_account in res.get('body').get('owned_ad_accounts').get('data'):
            owned_ad_accounts_ids.append(ad_account.get('id'))
            ASSETS_IDS.append(ad_account.get('id'))

        owned_pages_ids = list()
        if (res.get('body') is not None) and (res.get('body').get('owned_pages') is not None) and (
                res.get('body').get('owned_pages').get('data') is not None):
            for page in res.get('body').get('owned_pages').get('data'):
                owned_pages_ids.append(page.get('id'))
                ASSETS_IDS.append(page.get('id'))

        # *** STEP 1 ***
        # This creates an relationship edge between partner's Business Manager and client's Business Manager.
        # This enables the partner to be able to create a SU via the API in the next step

        params = {
            'existing_client_business_id': CLIENT_BM_ID,
            'access_token': client_admin_access_token
        }
        res = requests.post('https://graph.facebook.com/v13.0/' + str(PARTNER_BM_ID) + '/managed_businesses', params)
        if res.status_code != 200:
            return {"status": res.status_code, "body": res.json()}

        # *** STEP 2 ***
        # Fetch the access token of system user under the client's Business Manager
        PARTNER_BM_ADMIN_SYSTEM_USER_ACCESS_TOKEN = client_admin_access_token  # fixed! todo: fetch PARTNER_BM_ADMIN_SYSTEM_USER_ACCESS_TOKEN

        params = {
            'scope': "ads_management,pages_read_engagement,ads_read,business_management",
            'app_id': str(OQ_app_id),
            'access_token': PARTNER_BM_ADMIN_SYSTEM_USER_ACCESS_TOKEN
        }
        res = requests.post('https://graph.facebook.com/v13.0/' + CLIENT_BM_ID + '/access_token', params)
        if res.status_code != 200:
            return {"status": res.status_code, "body": res.json()}

        # The response contains the token for the system user who is linked to the On Behalf Of relationships.
        CLIENT_BM_SU_ACCESS_TOKEN = res.json().get('access_token')  # fixed! todo: get this system user token

        # *** STEP 3 ***
        # Get the ID of the system user.
        params = {
            'access_token': CLIENT_BM_SU_ACCESS_TOKEN
        }
        res = requests.get('https://graph.facebook.com/v13.0/me', params)
        if res.status_code != 200:
            return {"status": res.status_code, "body": res.json()}
        SYSTEM_USER_ID = res.json().get('id')

        # *** STEP 4 ***
        # Assign assets to the system user in the client's Business Manager.
        ad_accounts_in_DB = list()
        for ad_account_record in db.getFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(CLIENT_BM_ID):
            ad_accounts_in_DB.append(ad_account_record[1])

        pages_in_DB = list()
        for page_record in db.getFB_CLIENT_PAGES_BY_BM_ID(CLIENT_BM_ID):
            pages_in_DB.append(page_record[1])

        for asset in owned_ad_accounts_ids:
            params = {
                "user": SYSTEM_USER_ID,
                "tasks": "MANAGE",
                'access_token': client_admin_access_token
            }
            # time.sleep(2)
            res = requests.post('https://graph.facebook.com/v13.0/' + asset + '/assigned_users', params)
            if res.status_code != 200:
                return {"status": res.status_code, "body": res.json()}
            if asset not in ad_accounts_in_DB:
                db.addFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(CLIENT_BM_ID, asset)

        for asset in owned_pages_ids:
            params = {
                "user": SYSTEM_USER_ID,
                "tasks": "MANAGE",
                'access_token': client_admin_access_token
            }
            # time.sleep(2)
            res = requests.post('https://graph.facebook.com/v13.0/' + asset + '/assigned_users', params)
            if res.status_code != 200:
                return {"status": res.status_code, "body": res.json()}
            if asset not in pages_in_DB:
                db.addFB_CLIENT_PAGES_BY_BM_ID(CLIENT_BM_ID, asset)

        owned_pixels_ids = list()
        pixels_res = Pixel.get_all_business_pixels(client_admin_access_token, CLIENT_BM_ID)
        if pixels_res.status_code != 200:
            return {"status": pixels_res.status_code, "body": pixels_res.json()}

        print("pixels_res: " + str(pixels_res.json()))

        if (pixels_res.json() is not None) and (pixels_res.json().get('owned_pixels') is not None) and (
                pixels_res.json().get('owned_pixels').get('data') is not None):
            for pixel in pixels_res.json().get('owned_pixels').get('data'):
                owned_pixels_ids.append(pixel.get('id'))
                ASSETS_IDS.append(pixel.get('id'))

        for asset in owned_pixels_ids:
            params = {
                "user": SYSTEM_USER_ID,
                "tasks": "EDIT, ANALYZE, UPLOAD, ADVERTISE, AA_ANALYZE",
                'access_token': client_admin_access_token
            }
            # time.sleep(2)
            res = requests.post('https://graph.facebook.com/v13.0/' + asset + '/assigned_users', params)
            if res.status_code != 200:
                return {"status": res.status_code, "body": res.json()}
            # if asset not in pages_in_DB: #todo
            #     db.addFB_CLIENT_PAGES_BY_BM_ID(CLIENT_BM_ID, asset)

        if CLIENT_BM_ID not in BMs_in_DB:
            db.addFB_CLIENT_BM_SU_ACCESS_TOKEN(oq_user_id, CLIENT_BM_ID, str(PARTNER_BM_ID), client_user_id,
                                               CLIENT_BM_SU_ACCESS_TOKEN)
        succeeded_BMs_id_list += CLIENT_BM_ID + ","

    # ** DONE: **
    # todo: save CLIENT_BM_SU_ACCESS_TOKEN in DB
    #  primary key: user ID is OQ system. save also FB_uid. save also CLIENT_BM_SU_ACCESS_TOKEN

    if len(succeeded_BMs_id_list) == 0:
        return {"status": 400, "body": {"No business added as a client"}}

    return {"status": 200, "body": {"client_businesses_added": succeeded_BMs_id_list}}