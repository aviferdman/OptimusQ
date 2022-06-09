CREATE TABLE LandingPage
(
	"URL" VARCHAR(256),
	"AdvertiserID" INTEGER,
	PRIMARY KEY ("URL","AdvertiserID"),
	FOREIGN KEY ("AdvertiserID") REFERENCES [dbo].[Advertisers]("ID")
);

CREATE TABLE "Keywords"
(
	"LandingPageURL" VARCHAR(256),
	"Keyword" VARCHAR(256),
	PRIMARY KEY ("LandingPageURL","Keyword"),
	FOREIGN KEY ("LandingPageURL") REFERENCES [dbo].[LandingPage]("URL")
);

CREATE TABLE "ImagesToKeyword"
(
	"ImageURL" VARCHAR(256),
	"Keyword" VARCHAR(256),
	PRIMARY KEY("ImageURL","Keyword"),
	FOREIGN KEY("ImageURL") REFERENCES [dbo].[Images]("ImageURL")
	FOREIGN KEY("Keyword") REFERENCES [dbo].[Keywords]("Keyword")
);

CREATE TABLE "LandingPageToKeyWord"
(
	"LandingPageURL" VARCHAR(256),
	"Keyword" VARCHAR(256),
	PRIMARY KEY("LandingPageURL","Keyword"),
	FOREIGN KEY("LandingPageURL") REFERENCES [dbo].[LandingPage]("URL"),
	FOREIGN KEY("Keyword") REFERENCES [dbo].[Keywords]("Keyword")
);

CREATE TABLE "UserAccessTokenByUserId"
(
	"UserId" VARCHAR(256),
	"AccessToken" VARCHAR(256),
	PRIMARY KEY("UserId")
);

CREATE TABLE "FB_Ad_Accounts"
(
	"id" VARCHAR(256),
	"name" VARCHAR(256),
	"business" VARCHAR(256),
    "amount_spent" INTEGER,
	PRIMARY KEY("id")
);

CREATE TABLE "FB_Campaigns"
(
	"id" VARCHAR(256),
    "ad_account" VARCHAR(256),
	"name" VARCHAR(256),
    "objective" VARCHAR(256),
    "status" VARCHAR(256),
	PRIMARY KEY("id"),
--     FOREIGN KEY("ad_account") REFERENCES [dbo].[FB_Ad_Accounts]("id")
);

CREATE TABLE "FB_AdSets"
(
	"id" VARCHAR(256),
    "ad_account" VARCHAR(256),
    "campaign" VARCHAR(256),
    "name" VARCHAR(256),
    "daily_budget" INTEGER,
    "targeting" VARCHAR(256),
	PRIMARY KEY("id"),
--     FOREIGN KEY("ad_account") REFERENCES [dbo].[FB_Ad_Accounts]("id"),
--     FOREIGN KEY("campaign") REFERENCES [dbo].[FB_Campaigns]("id")
);

CREATE TABLE "FB_Images"
(
    "hash" VARCHAR(512),
    "permalink_url" VARCHAR(512),
	PRIMARY KEY("hash")
);

CREATE TABLE "FB_AdCreatives"
(
	"id" VARCHAR(256),
    "name" VARCHAR(256),
    "title" VARCHAR(256),
    "body" VARCHAR(256),
    "image_hash" VARCHAR(512),
	PRIMARY KEY("id"),
--     FOREIGN KEY("image_hash") REFERENCES [dbo].[FB_Images]("hash")
);

CREATE TABLE "FB_Ads"
(
	"id" VARCHAR(256),
    "adSet" VARCHAR(256),
    "name" VARCHAR(256),
    "creative" VARCHAR(256),
    "status" VARCHAR(256),
	PRIMARY KEY("id"),
--     FOREIGN KEY("adSet") REFERENCES [dbo].[FB_AdSets]("id"),
--     FOREIGN KEY("creative") REFERENCES [dbo].[FB_AdCreatives]("id")
);

CREATE TABLE "FB_Targeting_Behaviors"
(
	"id" VARCHAR(512),
	"name" VARCHAR(512),
	"audience_size_lower_bound" VARCHAR(256),
	"audience_size_upper_bound" VARCHAR(256),
	"path" VARCHAR(512),
	"description" VARCHAR(512),
	PRIMARY KEY("id")
);

CREATE TABLE "GoogleAds_Tokens"
(
	"client_id" VARCHAR(512),
	"login_customer_id" VARCHAR(512),
	"developer_token" VARCHAR(512),
	"client_secret" VARCHAR(512),
	"refresh_token" VARCHAR(512),
	PRIMARY KEY("client_id","login_customer_id")
);

CREATE TABLE "FB_CLIENT_BM_SU_ACCESS_TOKEN" (
    "OQ_user_id" VARCHAR(512),
    "FB_client_BM_id" VARCHAR(512),
	"assigned_partner_id" VARCHAR(512),
	"FB_client_user_id" VARCHAR(512),
    "su_access_token" VARCHAR(512),
	PRIMARY KEY("OQ_user_id","FB_client_BM_id", "assigned_partner_id")
);

CREATE TABLE "FB_CLIENT_AD_ACCOUNTS_BY_BM_ID" (
    "FB_client_BM_id" VARCHAR(512),
    "Ad_Account_Id" VARCHAR(512),
	PRIMARY KEY("FB_client_BM_id","Ad_Account_Id")
);

CREATE TABLE "FB_CLIENT_PAGES_BY_BM_ID" (
    "FB_client_BM_id" VARCHAR(512),
    "Page_Id" VARCHAR(512),
	PRIMARY KEY("FB_client_BM_id","Page_Id")
);