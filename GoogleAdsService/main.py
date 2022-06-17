from DataBaseService.main import dataBaseController

db = dataBaseController

res1 = db.addGoogleAds_RS_Ad("c", "g", "a", "h", "d", "URL", "p")

res2 = db.getGoogleAds_RS_Ad("c", "g", "a")

res3 = db.getAllGoogleAds_RS_Ads("c", "g")

res4 = db.deleteGoogleAds_RS_Ad("c", "g", "a")