
# Recommendaion System

## Presentation Service
Responsible for using all services and presents them in a simple and user-friendly UI.
The UI can be found [here](https://scannerwebapp.azurewebsites.net/).
This repository is connected directly to the UI webApp so every update here is also performed there.

## Management Service 
The main service. Responsible for connecting all the services. Receives URL of a landing page and returns the following parameters: title, description, keywords and list of up to 5 recommended images. 

## Scanner Service
Responsible for extract data from a given landing page.
Contains the following:
- recoSystem.py: The main class that contains the functions of scraping a landing page
- response.py: Class for handling errors and returning appropriate messages to the user
- screenshot.py: Class for taking screenshot by the computer. Needs for the mission of scrap images and videos from a landing page

## Image Service
Responsible for recommending the photos after scanning the page.

## Databases Service
Responsible for connecting to a remote DataBases sitting on a cloud in Azure.

## Tests
- Unit tests: The tests available are for the following services: Scanner Service, Image Service and Databases Service.
- Integration tests: this tests testing the Management Service which is the package that connect all services.

## Documentation
Contains the following:
- Blocking-Diagram: Diagram of the principal parts of the system represented by blocks connected by lines that show the relationships of the blocks
- ReleaseNotes
- api-documentation



