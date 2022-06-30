import requests
import urllib.request

# ************ Image MANAGEMENT ************
# *********************************************

# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_path(access_token, AD_ACCOUNT_ID, image_path):
    access_token = access_token
    image_file = open(image_path, "rb")
    url = 'https://graph.facebook.com/v13.0/act_' + AD_ACCOUNT_ID + '/adimages'
    file_obj = {'filename': image_file}
    payload = {"access_token": access_token}
    return requests.post(url, data=payload, files=file_obj)


# adds an image to ad creative repository.
# image_path - path of image to upload, from local computer.
# returns image's hash
def upload_image_by_url(access_token, AD_ACCOUNT_ID, image_url):
    if "act_" not in AD_ACCOUNT_ID:
        AD_ACCOUNT_ID = "act_" + AD_ACCOUNT_ID
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    try:
        # request = urllib.request.Request(image_url, None, headers)  # The assembled request
        # response = urllib.request.urlopen(request)
        # data = response.read()  # The data we need
        # image_file = base64.b64encode(data).decode()
        url = 'https://graph.facebook.com/v13.0/' + AD_ACCOUNT_ID + '/adimages'

        urllib.request.urlretrieve(image_url, "local-img.jpg")
        image_file = open("local-img.jpg", "rb")

        file_obj = {'filename': image_file}
        payload = {"access_token": access_token}
        res = requests.post(url, data=payload, files=file_obj)
        if res.status_code == 200:
            img_hash = res.json().get('images').get('local-img.jpg').get('hash')
            return {"status": res.status_code, "body": {"hash": img_hash}}
        return {"status": res.status_code, "body": res.json()}
    except Exception as e:
        return {"status": 400, "body": str(e)}


# returns a A permanent URL of the image
def get_permanent_url_for_image_by_hash(access_token, ad_account, hash):
    fields = 'fields=permalink_url'
    params = {
        'hashes': str([hash]),
        'access_token': access_token
    }
    res = requests.get('https://graph.facebook.com/v13.0/act_' + ad_account + '/adimages?' +
                       fields, params)
    return {"status": res.status_code, "body": res.json()}