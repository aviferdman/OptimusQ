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


dataBaseController=DataBaseController()

def main_trigger(request: azure.functions.HttpRequest):
    dataBaseController.TriggerTransaction(request)