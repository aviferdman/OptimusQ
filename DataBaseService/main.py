import pyodbc
import datetime
import azure.functions
import json

#####################
# Basic Parameters  #
#####################
# password = '{avidorgilTheBest2022}'
# connectionString = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:optimusbgudb.database.windows.net,1433;Database=Optimus-BGU-db;Uid=Optimus-BGU-db;Pwd=' + \
#     password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'



class DataBaseController:
    def __init__(self):
        self.password='{avidorgilTheBest2022}'
        self.connectionString='Driver={ODBC Driver 17 for SQL Server};Server=tcp:optimusbgudb.database.windows.net,1433;Database=Optimus-BGU-db;Uid=Optimus-BGU-db;Pwd=' + \
        self.password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

    def TriggerTransaction(self,request: azure.functions.HttpRequest):
        try:
            theBody = request.get_json()
            theJson = theBody

            landingPage = theJson["landingPage"]
            keyWords = theJson["keywords"]
            description = theJson["description"]
            title = theJson["title"]
            images = theJson["images"]

            DEVELOPERS_ID = 1

            self.writIDconnection2db(DEVELOPERS_ID)
            self.writeLandingPage2db(landingPage, DEVELOPERS_ID)
            self.writeKeywords2db(keyWords)
            self.writeDescription2db(landingPage, title, description)
            self.writeLandingPageToKeyWord(landingPage, keyWords)
            self.writeImages2db(images)
            return "OK"

        except Exception as e:
            print(str(e))
            return "Empty body"

    ######################################################################
    #  Advertisers
    ######################################################################
    def getAdvertisersIDs(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT ID FROM Advertisers
                                """)
                myresult = cursor.fetchall()
                return myresult



    ######################################################################
    #  ID connections
    ######################################################################
    def writIDconnection2db(self,id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO
                    Connections(Date, AdvertiserID)
                    VALUES('{0}', {1});
                    """.format(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), id))

    def getIDconnections(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM Connections
                                """)
                myresult = cursor.fetchall()
                return myresult

    ######################################################################
    #  Landing Page
    ######################################################################

    def getAllLandingPages(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM LandingPage
                                """)
                myresult = cursor.fetchall()
                return myresult

    def getLandingPageByUrl(self,url):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM LandingPage
                                WHERE "URL"='{0}';
                                """.format(url))
                myresult = cursor.fetchall()
                return myresult

    def writeLandingPage2db(self,landing, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM LandingPage
                WHERE "URL"='{0}'
                """.format(landing))
                myresult = cursor.fetchall()
                if(len(myresult) == 0):
                    cursor.execute("""
                        INSERT INTO
                        LandingPage(URL, AdvertiserID)
                        VALUES('{0}', '{1}');
                        """.format(landing, id))

    ######################################################################
    #  Keywords
    ######################################################################

    def getAllKeyWords(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM Keywords
                                """)
                myresult = cursor.fetchall()
                return myresult

    def getKeyWordByKey(self,keyword):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM Keywords
                                WHERE "Keyword"='{0}';
                                """.format(keyword))
                myresult = cursor.fetchall()
                return myresult

    def writeKeywords2db(self,parm):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                for keyWord in parm:
                    cursor.execute("""
                    SELECT * FROM Keywords
                    WHERE "Keyword" = '{0}'
                    """.format(keyWord))

                    theResult = cursor.fetchall()
                    if(len(theResult) == 0):
                        cursor.execute("""
                            INSERT INTO
                            Keywords(KeyWord)
                            VALUES('{0}');
                            """.format(keyWord))

    ######################################################################
    #  Description
    ######################################################################

    def getDescriptionByURL(self,url):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM TitleAndDescription
                                WHERE "LandingPageURL"='{0}';
                                """.format(url))
                myresult = cursor.fetchall()
                return myresult

    def writeDescription2db(self,url, title, description):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM TitleAndDescription
                WHERE "LandingPageURL" = '{0}'
                """.format(url))

                theResult = cursor.fetchall()
                if(len(theResult) == 0):
                    cursor.execute("""
                        INSERT INTO
                        TitleAndDescription(LandingPageURL, Title,Description)
                        VALUES('{0}', '{1}','{2}');
                        """.format(url, title, description))

    ######################################################################
    #  LandingPage to keyword
    ######################################################################
    def writeLandingPageToKeyWord(self,url, keywords:[]):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                for keyword in keywords:
                    cursor.execute("""
                    SELECT * FROM [dbo].[LandingPageToKeyWord]
                    WHERE "LandingPageURL" = '{0}'
                    AND "Keyword" = '{1}';
                    """.format(url, keyword))

                    theResult = cursor.fetchall()
                    if(len(theResult) == 0):
                        cursor.execute("""
                            INSERT INTO
                            LandingPageToKeyWord(LandingPageURL, Keyword)
                            VALUES('{0}', '{1}');
                            """.format(url, keyword))

    def getLandingPageToKeyword(self,url,keyword):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM LandingPageToKeyWord
                                WHERE "LandingPageURL"='{0}'
                                AND "Keyword"='{1}';
                                """.format(url,keyword))
                myresult = cursor.fetchall()
                return myresult


    def writeImages2db(self,images):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                for keyword in images:
                    for url in images[keyword]:
                        cursor.execute("""
                        SELECT * FROM [dbo].[Images]
                        WHERE "ImageURL" = '{0}';
                        """.format(url))

                        theResultForImages = cursor.fetchall()

                        if(len(theResultForImages) == 0):
                            cursor.execute("""
                                INSERT INTO
                                Images(ImageURL)
                                VALUES('{0}');
                                """.format(url))

                        cursor.execute("""
                        SELECT * FROM [dbo].[ImagesToKeyword]
                        WHERE "ImageURL" = '{0}'
                        AND "Keyword" = '{1}';
                        """.format(url, keyword))

                        theResltForImageToKeyword = cursor.fetchall()

                        if(len(theResultForImages) == 0):
                            cursor.execute("""
                                INSERT INTO
                                ImagesToKeyword(ImageURL,Keyword)
                                VALUES('{0}','{1}');
                                """.format(url, keyword))

    ######################################################################
    #  UserAccessTokenByUserId
    ######################################################################

    def getAccessTokenByUserId(self, user_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM UserAccessTokenByUserId
                                WHERE "UserId"='{0}';
                                """.format(user_id))
                myresult = cursor.fetchall()
                return myresult

    def deleteAccessTokenByUserId(self, user_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM UserAccessTokenByUserId
                WHERE "UserId" = '{0}';
                """.format(user_id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM UserAccessTokenByUserId WHERE "UserId" = '{0}';
                        """.format(user_id))

    def writeAccessToken2db(self, user_id, access_token):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM UserAccessTokenByUserId
                WHERE "UserId" = '{0}';
                """.format(user_id))
                theResult = cursor.fetchall()
                if (len(theResult) == 0):
                    cursor.execute("""
                        INSERT INTO
                        UserAccessTokenByUserId(UserId, AccessToken)
                        VALUES('{0}', '{1}');
                        """.format(user_id, access_token))

    ######################################################################
    #  FB_Campaigns
    ######################################################################
    def addCampaign(self, id, ad_account, name, objective, status):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_Campaigns] (id, ad_account, name, objective, status)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');
                    """.format(id, ad_account, name, objective, status))

    def getCampaign(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_Campaigns
                                WHERE "id"='{0}';
                                """.format(id))
                myresult = cursor.fetchall()
                return myresult

    def getAllCampaigns(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Campaigns;""")
                myresult = cursor.fetchall()
                return myresult

    def deleteCampaign(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Campaigns
                WHERE "id" = '{0}';
                """.format(id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM FB_Campaigns WHERE "id" = '{0}';
                        """.format(id))



    ######################################################################
    #  FB_AdSets
    ######################################################################
    def addAdSet(self, id, ad_account, campaign, name, daily_budget, targeting):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_AdSets] (id, ad_account, campaign, name, daily_budget, targeting)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');
                    """.format(id, ad_account, campaign, name, daily_budget, targeting))

    def getAdSet(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_AdSets
                                WHERE "id"='{0}';
                                """.format(id))
                myresult = cursor.fetchall()
                return myresult

    def getAllAdSets(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_AdSets;""")
                myresult = cursor.fetchall()
                return myresult

    def deleteAdSet(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_AdSets
                WHERE "id" = '{0}';
                """.format(id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM FB_AdSets WHERE "id" = '{0}';
                        """.format(id))


    ######################################################################
    #  FB_Images
    ######################################################################
    def addFBImage(self, hash, permalink_url):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_Images] (hash, permalink_url)
                    VALUES ('{0}', '{1}');
                    """.format(hash, permalink_url))

    def getFBImage(self, hash):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_Images
                                WHERE "hash"='{0}';
                                """.format(hash))
                myresult = cursor.fetchall()
                return myresult

    def getAllFBImages(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Images;""")
                myresult = cursor.fetchall()
                return myresult

    def deleteFBImage(self, hash):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Images
                WHERE "hash" = '{0}';
                """.format(hash))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM FB_Images WHERE "hash" = '{0}';
                        """.format(hash))


    ######################################################################
    #  FB_AdCreatives
    ######################################################################
    def addFBAdCreative(self, id, name, title, body, image_hash):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_AdCreatives] (id, name, title, body, image_hash)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');
                    """.format(id, name, title, body, image_hash))

    def getFBAdCreative(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_AdCreatives
                                WHERE "id"='{0}';
                                """.format(id))
                myresult = cursor.fetchall()
                return myresult

    def getAllFBAdCreatives(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_AdCreatives;""")
                myresult = cursor.fetchall()
                return myresult

    def deleteFBAdCreative(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_AdCreatives
                WHERE "id" = '{0}';
                """.format(id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM FB_AdCreatives WHERE "id" = '{0}';
                        """.format(id))


    ######################################################################
    #  FB_Ads
    ######################################################################
    def addFBAd(self, id, adSet, name, creative, status):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_Ads] (id, adSet, name, creative, status)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');
                    """.format(id, adSet, name, creative, status))

    def getFBAd(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_Ads
                                WHERE "id"='{0}';
                                """.format(id))
                myresult = cursor.fetchall()
                return myresult

    def getAllFBAds(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Ads;""")
                myresult = cursor.fetchall()
                return myresult

    def deleteFBAd(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Ads
                WHERE "id" = '{0}';
                """.format(id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM FB_Ads WHERE "id" = '{0}';
                        """.format(id))

    ######################################################################
    #  GoogleAds_Tokens
    ######################################################################
    def get_GoogleAds_Token(self, client_id, login_customer_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM GoogleAds_Tokens
                                WHERE "client_id"='{0}'
                                AND "login_customer_id"='{1}';
                                """.format(client_id, login_customer_id))
                myresult = cursor.fetchall()[0]
                res = {"developer_token": myresult[2], "client_secret": myresult[3], "refresh_token": myresult[4]}
                return res

    ######################################################################
    #  FB_Targeting_Behaviors
    ######################################################################
    def addFBTargetingBehavior(self, id, name, audience_size_lower_bound, audience_size_upper_bound, path, description):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_Targeting_Behaviors] (id, name, audience_size_lower_bound, audience_size_upper_bound, path, description)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');
                    """.format(id, name, audience_size_lower_bound, audience_size_upper_bound, path, description))

    def getFBTargetingBehaviorById(self, id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_Targeting_Behaviors
                                WHERE "id"='{0}';
                                """.format(id))
                myresult = cursor.fetchall()
                return myresult

    def getAllFBTargetingBehaviors(self):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM FB_Targeting_Behaviors;""")
                myresult = cursor.fetchall()
                return myresult

    ######################################################################
    #  FB_CLIENT_BM_SU_ACCESS_TOKEN
    ######################################################################
    def addFB_CLIENT_BM_SU_ACCESS_TOKEN(self, OQ_user_id, FB_client_BM_id, assigned_partner_id, FB_client_user_id, su_access_token):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_CLIENT_BM_SU_ACCESS_TOKEN] (OQ_user_id, FB_client_BM_id, assigned_partner_id, FB_client_user_id, su_access_token)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');
                    """.format(OQ_user_id, FB_client_BM_id, assigned_partner_id, FB_client_user_id, su_access_token))

    def getFB_CLIENT_BM_IDS_BY_OQ_USER_ID(self, OQ_user_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_CLIENT_BM_SU_ACCESS_TOKEN
                                WHERE "OQ_user_id"='{0}';
                                """.format(OQ_user_id))
                myresult = cursor.fetchall()
                return myresult

    def getFB_CLIENT_TOKEN_BY_OQ_USER_ID_AND_BM_ID(self, OQ_user_id, FB_client_BM_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_CLIENT_BM_SU_ACCESS_TOKEN
                                WHERE "OQ_user_id"='{0}' and "FB_client_BM_id"='{1}';
                                """.format(OQ_user_id, FB_client_BM_id))
                myresult = cursor.fetchall()
                return myresult

    ######################################################################
    #  FB_CLIENT_AD_ACCOUNTS_BY_BM_ID
    ######################################################################
    def addFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(self, FB_client_BM_id, Ad_Account_Id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_CLIENT_AD_ACCOUNTS_BY_BM_ID] (FB_client_BM_id, Ad_Account_Id)
                    VALUES ('{0}', '{1}');
                    """.format(FB_client_BM_id, Ad_Account_Id))

    def getFB_CLIENT_AD_ACCOUNTS_BY_BM_ID(self, FB_client_BM_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_CLIENT_AD_ACCOUNTS_BY_BM_ID
                                WHERE "FB_client_BM_id"='{0}';
                                """.format(FB_client_BM_id))
                myresult = cursor.fetchall()
                return myresult

    ######################################################################
    #  FB_CLIENT_PAGES_BY_BM_ID
    ######################################################################
    def addFB_CLIENT_PAGES_BY_BM_ID(self, FB_client_BM_id, Page_Id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[FB_CLIENT_PAGES_BY_BM_ID] (FB_client_BM_id, Page_Id)
                    VALUES ('{0}', '{1}');
                    """.format(FB_client_BM_id, Page_Id))

    def getFB_CLIENT_PAGES_BY_BM_ID(self, FB_client_BM_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM FB_CLIENT_PAGES_BY_BM_ID
                                WHERE "FB_client_BM_id"='{0}';
                                """.format(FB_client_BM_id))
                myresult = cursor.fetchall()
                return myresult



    ######################################################################
    #  GoogleAds_Tokens
    ######################################################################
    def get_GoogleAds_Token(self, client_id, login_customer_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM GoogleAds_Tokens
                                WHERE "client_id"='{0}'
                                AND "login_customer_id"='{1}';
                                """.format(client_id, login_customer_id))
                myresult = cursor.fetchall()[0]
                res = {"developer_token": myresult[2], "client_secret": myresult[3], "refresh_token": myresult[4]}
                return res


    ######################################################################
    #  GoogleAds_Campaigns
    ######################################################################
    def addGoogleAds_Campaign(self, customer_id, campaign_id, budget, name, start_date,
                               end_date,status,delivery_method,period,advertising_channel_type,
                               payment_mode,targeting_locations,targeting_country_codes,targeting_gender,targeting_device_type,
                               targeting_min_age,targeting_max_age,targeting_interest):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[GoogleAds_Campaigns] (customer_id, campaign_id, budget, name, start_date,
                               end_date,status,delivery_method,period,advertising_channel_type,
                               payment_mode,targeting_locations,targeting_country_codes,targeting_gender,targeting_device_type,
                               targeting_min_age,targeting_max_age,targeting_interest)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}','{14}','{15}', '{16}', '{17}');
                    """.format(customer_id, campaign_id, budget, name, start_date,
                               end_date,status,delivery_method,period,advertising_channel_type,
                               payment_mode,targeting_locations,targeting_country_codes,targeting_gender,targeting_device_type,
                               targeting_min_age,targeting_max_age,targeting_interest))

    def getGoogleAds_Campaign(self, customer_id, campaign_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM GoogleAds_Campaigns
                                WHERE "customer_id"='{0}' and "campaign_id"='{1}';
                                """.format(customer_id, campaign_id))
                myresult = cursor.fetchall()
                return myresult

    def getAllGoogleAds_Campaigns_By_Customer_Id(self, customer_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAds_Campaigns
                WHERE "customer_id"='{0}';""".format(customer_id))
                myresult = cursor.fetchall()
                return myresult

    def deleteGoogleAds_Campaign(self, customer_id, campaign_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAds_Campaigns
                WHERE "customer_id"='{0}' and "campaign_id"='{1}';
                """.format(customer_id, campaign_id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM GoogleAds_Campaigns WHERE "customer_id"='{0}' and "campaign_id"='{1}';
                        """.format(customer_id, campaign_id))


    ######################################################################
    #  GoogleAd_Groups
    ######################################################################
    def addGoogleAd_Group(self, customer_id, ad_group_id, campaign_id, name, cpc_bid, status):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[GoogleAd_Groups] (customer_id, ad_group_id, campaign_id, name, cpc_bid, status)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');
                    """.format(customer_id, ad_group_id, campaign_id, name, cpc_bid, status))

    def getGoogleAd_Group(self, customer_id, ad_group_id, campaign_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM GoogleAd_Groups
                                WHERE "customer_id"='{0}' and "ad_group_id"='{1}' and "campaign_id"='{2}';
                                """.format(customer_id, ad_group_id, campaign_id))
                myresult = cursor.fetchall()
                return myresult

    def getAllGoogleAd_Groups(self, customer_id, campaign_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAd_Groups
                WHERE "customer_id"='{0}' and "campaign_id"='{1}';""".format(customer_id, campaign_id))
                myresult = cursor.fetchall()
                return myresult

    def deleteGoogleAd_Group(self, customer_id, ad_group_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAd_Groups
                WHERE "customer_id"='{0}' and "ad_group_id"='{1}';
                """.format(customer_id, ad_group_id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM GoogleAd_Groups WHERE "customer_id"='{0}' and "ad_group_id"='{1}';
                        """.format(customer_id, ad_group_id))

    ######################################################################
    #  GoogleAds_Keywords
    ######################################################################
    def addGoogleAds_Keywords(self, customer_id, ad_group_id, criterion_id, keyword_text):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[GoogleAds_Keywords] (customer_id, ad_group_id, criterion_id, keyword_text)
                    VALUES ('{0}', '{1}', '{2}', '{3}');
                    """.format(customer_id, ad_group_id, criterion_id, keyword_text))

    def getAllGoogleAds_Keywords(self, customer_id, ad_group_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAds_Keywords
                WHERE "customer_id"='{0}' and "ad_group_id"='{1}';""".format(customer_id, ad_group_id))
                myresult = cursor.fetchall()
                return myresult

    def deleteGoogleAds_Keyword(self, customer_id, ad_group_id, criterion_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAds_Keywords
                WHERE "customer_id"='{0}' and "ad_group_id"='{1}' and "criterion_id"='{2}';
                """.format(customer_id, ad_group_id, criterion_id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM GoogleAds_Keywords WHERE "customer_id"='{0}' and "ad_group_id"='{1}' and "criterion_id"='{2}';
                        """.format(customer_id, ad_group_id, criterion_id))

    ######################################################################
    #  GoogleAds_RS_Ads
    ######################################################################
    def addGoogleAds_RS_Ad(self, customer_id, ad_group_id, ad_id, headlines_texts, descriptions_texts,
                           final_url, pinned_text):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [dbo].[GoogleAds_RS_Ads] (customer_id, ad_group_id, ad_id, headlines_texts, descriptions_texts,
                           final_url, pinned_text)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');
                    """.format(customer_id, ad_group_id, ad_id, headlines_texts, descriptions_texts,
                           final_url, pinned_text))

    def getGoogleAds_RS_Ad(self, customer_id, ad_group_id, ad_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                                SELECT * FROM GoogleAds_RS_Ads
                                WHERE "customer_id"='{0}' and "ad_group_id"='{1}' and "ad_id"='{2}';
                                """.format(customer_id, ad_group_id, ad_id))
                myresult = cursor.fetchall()
                return myresult

    def getAllGoogleAds_RS_Ads(self, customer_id, ad_group_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAds_RS_Ads
                WHERE "customer_id"='{0}' and "ad_group_id"='{1}';""".format(customer_id, ad_group_id))
                myresult = cursor.fetchall()
                return myresult

    def deleteGoogleAds_RS_Ad(self, customer_id, ad_group_id, ad_id):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM GoogleAds_RS_Ads
                WHERE "customer_id"='{0}' and "ad_group_id"='{1}' and "ad_id"='{2}';
                """.format(customer_id, ad_group_id, ad_id))
                theResult = cursor.fetchall()
                if (len(theResult) > 0):
                    cursor.execute("""
                        DELETE FROM GoogleAds_RS_Ads WHERE "customer_id"='{0}' and "ad_group_id"='{1}' and "ad_id"='{2}';
                        """.format(customer_id, ad_group_id, ad_id))


dataBaseController=DataBaseController()

def main_trigger(request: azure.functions.HttpRequest):
    dataBaseController.TriggerTransaction(request)