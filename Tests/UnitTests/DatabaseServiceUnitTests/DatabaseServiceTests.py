import time
import unittest

from DataBaseService.main import DataBaseController


class DbTestCase(unittest.TestCase):
    def setUp(self):
        self.db=DataBaseController()

    def test_WriteConnectionToDB_Success(self):
        success = True
        try:
            theResult=self.db.getIDconnections()
            countBefore=len(theResult)
            self.db.writIDconnection2db(1)
            theResult = self.db.getIDconnections()
            countAfter=len(theResult)
            self.assertTrue(success)
            self.assertGreaterEqual(countAfter,1)
            self.assertGreaterEqual(countAfter,countBefore)

        except Exception as e:
            success = False
    def GetUnknownID(self):
        connections = self.db.getAdvertisersIDs()
        id = 0
        for item in connections:
            if (item.ID > id):
                id = item.ID
        return id

    def test_WriteConnectionToDB_Fail(self):
        success = True
        try:
            self.db.writIDconnection2db(-1)
            success=False
        except Exception as e:
            success = True


        self.assertTrue(success)

        try:
            unknownID = self.GetUnknownID()
        except:
            success=False
        self.assertTrue(success)
        if(not success):
            return
        try:
            self.db.writIDconnection2db(unknownID+1)
            success=False
        except:
            success=True

        self.assertTrue(success)

    def test_ReadFromConnections(self):
        theConnections=self.db.getIDconnections()
        firstLen=len(theConnections)
        self.db.writIDconnection2db(1)
        time.sleep(1)
        self.db.writIDconnection2db(1)
        time.sleep(1)
        self.db.writIDconnection2db(1)

        theConnections = self.db.getIDconnections()
        second = len(theConnections)
        self.assertEqual(second,firstLen+3)



    def test_AddLandingPages(self):
        landingPages=self.db.getAllLandingPages()
        if(len(landingPages)>0):
            firstLandingPage=landingPages[0]
            firstLen=len(landingPages)
            success=True
            try:
                firstURL=firstLandingPage.URL
                firstAdID=firstLandingPage.AdvertiserID
                self.db.writeLandingPage2db(firstURL,firstAdID)
                success=True
                landingPages=self.db.getAllLandingPages()
            except:
                success=False

            secondLen=len(landingPages)

            self.assertTrue(success)
            self.assertEqual(secondLen,firstLen)
            try:
                firstURL+="aa"
                check=self.db.getLandingPageByUrl(firstURL)
                while(len(check)>0):
                    firstURL += "aa"
                    check = self.db.getLandingPageByUrl(firstURL)

                self.db.writeLandingPage2db(firstURL,firstAdID)

                check = self.db.getLandingPageByUrl(firstURL)

                self.assertEqual(len(check),1)
            except:
                self.assertTrue(False,"Failed")
        else:
            try:
                firstURL="aa"
                advertisers=self.db.getAdvertisersIDs()
                if(len(advertisers)==0):
                    self.assertTrue(True)
                    return
                firstAdID=advertisers[0].ID
                self.db.writeLandingPage2db(firstURL, firstAdID)
                check = self.db.getLandingPageByUrl(firstURL)
                self.assertEqual(len(check),1)
                return True
            except:
                self.assertTrue(False,"Failed")
        return firstURL

    def test_AddLandingPageOfUnknownAdvertiser(self):
        unknownID=self.GetUnknownID()
        success=True
        try:
            self.db.getLandingPageByUrl("aa",unknownID)
            success=False
        except:
            success=True

        self.assertTrue(success)

    def test_AddKeyWords_Success(self):
        try:
            allKeywords=self.db.getAllKeyWords()
            if(len(allKeywords)==0):
                self.db.writeKeywords2db(["a"])
                allKeywords=self.db.getAllKeyWords()
                self.assertGreaterEqual(len(allKeywords),0)
            else:
                firstKeyword=allKeywords[0].Keyword
                self.db.writeKeywords2db([firstKeyword])
                allKeywords2=self.db.getAllKeyWords()
                self.assertEqual(len(allKeywords),len(allKeywords2))
                while(len(self.db.getKeyWordByKey(firstKeyword))>0):
                    firstKeyword+="a"
                self.db.writeKeywords2db([firstKeyword])
                self.assertEqual(len(self.db.getAllKeyWords()),len(allKeywords2)+1)
        except:
            self.assertTrue(False)

    def test_WriteDescription_Success(self):
        landingPages=self.db.getAllLandingPages()
        if(len(landingPages)>0):
            lPage=landingPages[0].URL
            id=landingPages[0].AdvertiserID
            success=True
            try:
                self.db.writeDescription2db(lPage+"A","TestTitle","TestDescription")
                success=False
            except:
                success=True
            self.assertTrue(success)

        newURL=self.test_AddLandingPages()
        try:
            self.db.writeDescription2db(newURL , "TestTitle", "TestDescription")

            result=self.db.getDescriptionByURL(newURL)
            self.assertEqual(len(result),1)
            result0=result[0]
            self.assertEqual(result0.Title,"TestTitle")
            self.assertEqual(result0.Description,"TestDescription")
        except:
            self.assertTrue(False)

    def test_WriteLandingPageToKeyword(self):
        landingPages=self.db.getAllLandingPages()
        keywords=self.db.getAllKeyWords()
        if(len(landingPages)==0 or len(keywords)==0):
            if(len(landingPages)==0):
                self.db.writeLandingPage2db("LandingTest",1)
                landingPages=self.db.getAllLandingPages()
                self.assertGreater(len(landingPages),0)

            if(len(keywords)==0):
                self.db.writeKeywords2db(["TestKeyword"])
                keywords=self.db.getAllKeyWords()
                self.assertGreater(len(keywords),0)

        selectedKey=0
        selectedLp=0
        found=False

        #find in db landing page and keyword that doesn't have match
        for keyword in keywords:
            if(found):
                break
            for lp in landingPages:
                if(found):
                    break
                if(len(self.db.getLandingPageToKeyword(lp.URL,keyword.Keyword))==0):
                    found=True
                    selectedKey=keyword.Keyword
                    selectedLp=lp.URL

        if(found == False):
            self.db.writeLandingPage2db("LandingTest2", 1)
            landingPages = self.db.getLandingPageByUrl("LandingTest2")
            self.assertGreater(len(landingPages),0)
            self.db.writeKeywords2db(["TestKeyword2"])
            keywords = self.db.getKeyWordByKey("TestKeyword2")
            self.assertGreater(len(keywords),0)

            self.db.writeLandingPageToKeyWord("LandingTest2","TestKeyword2")
            result=self.db.getLandingPageToKeyword("LandingTest2","TestKeyword2")

            self.assertGreater(len(result),0)

        else:
            self.db.writeLandingPageToKeyWord(selectedLp, [selectedKey])
            result = self.db.getLandingPageToKeyword(selectedLp,selectedKey)
            self.assertGreater(len(result),0)




if __name__=="__main__":
    unittest.main()
