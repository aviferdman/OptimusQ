import pyodbc
import datetime
import azure.functions
import json

#####################
# Basic Parameters  #
#####################
password = '{avidorgilTheBest2022}'
connectionString = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:optimusbgudb.database.windows.net,1433;Database=Optimus-BGU-db;Uid=Optimus-BGU-db;Pwd=' + \
    password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


def main_trigger(request: azure.functions.HttpRequest):
    try:
        theBody = request.get_json()
        theJson = theBody

        landingPage = theJson["landingPage"]
        keyWords = theJson["keywords"]
        description = theJson["description"]
        title = theJson["title"]
        images = theJson["images"]

        DEVELOPERS_ID = 1

        writIDconnection2db(DEVELOPERS_ID)
        writeLandingPage2db(landingPage, DEVELOPERS_ID)
        writeKeywords2db(keyWords)
        writeDescription2db(landingPage, title, description)
        writeLandingPageToKeyWord(landingPage, keyWords)
        writeImages2db(images)
        return "OK"

    except Exception as e:
        print(str(e))
        return "Empty body"


def writIDconnection2db(id):
    with pyodbc.connect(connectionString) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO
                Connections(Date, AdvertiserID)
                VALUES('{0}', {1});
                """.format(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), id))


def writeLandingPage2db(landing, id):
    with pyodbc.connect(connectionString) as conn:
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


def writeKeywords2db(parm):
    with pyodbc.connect(connectionString) as conn:
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


def writeDescription2db(url, title, description):
    with pyodbc.connect(connectionString) as conn:
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


def writeLandingPageToKeyWord(url, keywords):
    with pyodbc.connect(connectionString) as conn:
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


def writeImages2db(images):
    with pyodbc.connect(connectionString) as conn:
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
