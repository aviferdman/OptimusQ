
OptimusQ-BGU version 1.0
December 27, 2021

<h1> Release Notes: </h1>

<h3> Scanner Service </h3>

<h4> Objective: Extract keywords from a valid landing page </h4>

* [feature] able to get landing page URL to extract keywords by 'BeautifulSoup' library:

       1. First, trying to find tag of 'keywords' in the HTML page of the landing page.

       2. If there is no tag like this, find the keywords by 'yake' library and by
           an algorithm we wrote. 

* [bugfix] enter invalid landing page URL shows an appropriate message to the user.

<h4> Objective: Extract title from a valid landing page </h4>

* [Add] able to get landing page URL to extract title from the HTML page by scanning the tags.
* [bugfix] enter invalid landing page URL shows an appropriate message to the user.
* [bugfix] for landing page without tag of 'title' in its HTML page, the user gets an appropriate message.

<h4> Objective: Extract description from a valid landing page </h4>

* [Add] able to get landing page URL to extract description from the HTML page by scanning the tags.
* [bugfix] enter invalid landing page URL shows an appropriate message to the user.
* [bugfix] for landing page without tag of 'description' in its HTML page, the user gets an appropriate message.

<h3> Image Service </h3>

<h4> Objective: Retrieve images from image servers according to keywords: </h4>

* [Add] method to retrieve images from image servers, currently supports Shutterstock and Pixable.
* [feature] able to receive a dictionary of properties in last arguments to optimize the search according to properties values.
* [bugfix] Balancing requests to Shutterstock.

<h3> Management Service </h3>

<h4> Objective: Managing communication between Scanner and Images modules: </h4>

* [Add] Communication management between modules
* [Add] Exposing the main external API of the version

<h3> Azure Services </h3>

<h4> Objective: Using serverless methodologies, azure functions. </h4>

* [Add] each module has an API exported via azure function API
* [Add] the Management Service module has the main API which calls the other services.
* [Add] the service web on azure is connected to the git repository and responsible on the UI. This service uses the Management Service API.
* [Add] Azure SQL database as the database of the system aims to record keywords, titles, descriptions, images, and landing pages.

<h4> The data base we are using: </h4> 
*	Sql Server
*	Microsoft Azure
*	Server name: Optimus-BGU-db
*	Connectivity is done using database module


<h3> Version Control </h3>

<h4> Objective: Managing code, versions, documentations in GitHub: </h4> 

* [Add] All source code in GitHub.
* [Add] All unit & integration tests for each module.
* [Add] Release note in v0.1 description.

<h3> DB: </h3>

<h4> Objective: Remote recording of data. </h4> 

* [Add] storing Advertisers information in Advertisers table.
* [Add] storing Records of date and time of users logins in Connections table.
* [Add] storing Images URLs that received from searching (using images databases API's) in Images table.
* [Add] storing Cross-references between Images URL's and the keywords used to search them, in ImagesToKeyword table.
* [Add] storing Keywords used in searches, in Keywords table.
* [Add] storing URLs of landing pages, given by advertisers, in LandingPage table.
* [Add] storing Cross-references between URL of landing page to keywords, extracted from scarpping the landing page, in LandingPageToKeyWord table.
* [Add] storing inf, Cross-references between URL of landing page to information about the creative- title and description, in TitleAndDescription table.

<h3> Client </h3>

<h4> Objective: Simple usable client: </h4> 

* [Add] Main page of app demo, including searching box for URL.
* [Add] Outcome's page listing: titles, descriptions, keywords, images

<h3> Unit tests </h3>

<h4> Objective: Testing each module thoroughly, separated from whole system. </h4> 

* [Add] Scanner Service unit testing
* [Add] Image Service unit testing
* [Add] DB Service unit testing

<h3> Integration tests </h3>

<h4> Objective: Integrating services testing:  </h4> 

* [Add] extensive integration tests between all modules.  

<h3> API Documentation </h3>

<h4> Objective: Services documentation. </h4>

* [Add] Detailed API for every service our system supplies.
Available in this link.

