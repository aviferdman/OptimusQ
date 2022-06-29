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

CREATE TABLE "GoogleAds_Tokens"
(
	"client_id" VARCHAR(512),
	"login_customer_id" VARCHAR(512),
	"developer_token" VARCHAR(512),
	"client_secret" VARCHAR(512),
	"refresh_token" VARCHAR(512),
	PRIMARY KEY("client_id","login_customer_id")
);

CREATE TABLE "GoogleAds_Campaigns"
(
	"customer_id" VARCHAR(40),
	"campaign_id" VARCHAR(250),
	"budget" INTEGER,
	"name" VARCHAR(250),
	"start_date" VARCHAR(250),
	"end_date" VARCHAR(250),
    "status" VARCHAR(250),
    "delivery_method" VARCHAR(250),
    "period" VARCHAR(250),
    "advertising_channel_type" VARCHAR(250),
    "payment_mode" VARCHAR(250),
    "targeting_locations" VARCHAR(520),
    "targeting_country_codes" VARCHAR(520),
    "targeting_gender" VARCHAR(250),
    "targeting_device_type" VARCHAR(250),
    "targeting_min_age" VARCHAR(250),
    "targeting_max_age" VARCHAR(250),
    "targeting_interest" VARCHAR(250),
	PRIMARY KEY("customer_id","campaign_id")
);

CREATE TABLE "GoogleAd_Groups"
(
	"customer_id" VARCHAR(40),
	"ad_group_id" VARCHAR(250),
	"campaign_id" VARCHAR(250),
	"name" VARCHAR(250),
	"cpc_bid" INTEGER,
	"status" VARCHAR(250),
	PRIMARY KEY("customer_id","ad_group_id")
);

CREATE TABLE "GoogleAds_Keywords"
(
	"customer_id" VARCHAR(40),
	"ad_group_id" VARCHAR(250),
	"criterion_id" VARCHAR(250),
	"keyword_text" VARCHAR(500),
	PRIMARY KEY("customer_id","ad_group_id", "criterion_id")
);

CREATE TABLE "GoogleAds_RS_Ads"
(
	"customer_id" VARCHAR(40),
	"ad_group_id" VARCHAR(250),
	"ad_id" VARCHAR(250),
	"headlines_texts" VARCHAR(250),
	"descriptions_texts" VARCHAR(500),
	"final_url" VARCHAR(500),
	"pinned_text" VARCHAR(500),
	PRIMARY KEY("customer_id","ad_group_id", "ad_id")
);