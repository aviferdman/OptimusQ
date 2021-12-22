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