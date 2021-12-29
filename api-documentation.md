# OPTIMUS-Q-BGU API's Documentation

These docs describe how to use the https://optimusqbgu.azurewebsites.net API. We hope you enjoy these docs.

## Creative - Get

```http
GET /api/managementservice
```

## URI Parameters
Name | In | Required | Type | Description |
| :--- | :--- | :--- | :--- | :--- | 

None URI Parameters in this API.

## Request Body
Name | Required | Type | Description |
| :--- | :--- | :--- | :--- | 
stock |	True | String |	Image repository. Must be either “pixable” or “shutterstock”
landingPage |	True | String | Valid landing page URL
imageServiceProperties | False | ImagePropertiesPixable / ImagePropertiesShutterstock | Any additional requirements for the images

## Responses
Name | Type | Description |
| :--- | :--- | :--- |
200 OK | Creative | OK response definition.

## Examples

### Example 1:
Request:
```javascript
{
  "stock": "shutterstock",
  "landingPage": "https://www.bbc.com/storyworks/clear-sky-thinking-airbus-2021/airbus-2021-clear-sky-thinking-?utm_source=taboola&utm_medium=native&tblci=GiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ#tblciGiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ"
}
```
Response:

Status code: 200
```javascript
{
  "title": "Clear Sky Thinking  | Clear Sky Thinking, Airbus 2021 | BBC StoryWorks",
  "description": "Cannot extract description",
  "keywords": [
        "airbus",
        "hydrogen",
        "global",
        "aviation",
        "aircraft",
        "saf",
        "towing vehicles",
        "semi-robotic towing",
        "emissions",
        "aerospace",
        "industry",
        "air",
        "solutions",
        "energy",
        "sustainable",
        "sustainable aviation",
        "airbus summit",
        "fuel",
        "aircraft taxi",
        "airbus recently"
    ],
  "images": {
        "airbus": [
            "https://image.shutterstock.com/display_pic_with_logo/228984501/1889697850/stock-photo-zoom-photo-of-airbus-a-passenger-airplane-taking-off-in-deep-blue-sky-and-beautiful-clouds-1889697850.jpg"
        ],
        "hydrogen": [
            "https://image.shutterstock.com/display_pic_with_logo/301517351/1739405825/stock-vector-hydrogen-tank-icon-simple-outline-colored-vector-of-sustainable-energy-icons-for-ui-and-ux-1739405825.jpg"
        ],
        "global": [
            "https://image.shutterstock.com/display_pic_with_logo/162718586/287193896/stock-photo-close-up-of-businessman-hand-showing-texture-the-world-with-digital-social-media-network-diagram-287193896.jpg"
        ],
        "aviation": [
            "https://image.shutterstock.com/display_pic_with_logo/250738318/1859181214/stock-photo-wide-shot-of-engineers-assembling-an-engine-of-a-passenger-jet-at-a-hangar-1859181214.jpg"
        ],
        "aircraft": [
            "https://image.shutterstock.com/display_pic_with_logo/250738318/1859178628/stock-photo-wide-shot-of-an-engineer-repairing-the-wing-of-a-passenger-jet-at-a-hangar-1859178628.jpg"
        ]
    }

}
```

### Example 2:
Request:
```javascript
{
  "stock": "pixable",
  "landingPage": "https://www.bbc.com/storyworks/clear-sky-thinking-airbus-2021/airbus-2021-clear-sky-thinking-?utm_source=taboola&utm_medium=native&tblci=GiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ#tblciGiDbJRndUImP9rc80Mls7KW1gFpDdEMCGlkTelmGFUrFzyCLjFQojKLYzprtvuKHAQ",
  "imageServiceProperties": {
        "colors": "yellow"
  }
}
```
Response:

Status code: 200
```javascript
{
  "title": "Clear Sky Thinking  | Clear Sky Thinking, Airbus 2021 | BBC StoryWorks",
  "description": "Cannot extract description",
  "keywords": [
        "airbus",
        "hydrogen",
        "global",
        "aviation",
        "aircraft",
        "saf",
        "towing vehicles",
        "semi-robotic towing",
        "emissions",
        "aerospace",
        "industry",
        "air",
        "solutions",
        "energy",
        "sustainable",
        "sustainable aviation",
        "airbus summit",
        "fuel",
        "aircraft taxi",
        "airbus recently"
    ],
  "images": {
        "global": [
            "https://pixabay.com/get/g59d2167199df77c6ffbc8652ca9275ee935a4658658ccd567c872a9a6e7c47a8cf9c42b8d98760fdafb3e2f096efdcd552c2bbed0e6aa03840869f8d40dfabdd_640.jpg"
        ],
        "aircraft": [
            "https://pixabay.com/get/ga8d5a8c3834746436ee881e00049e7889ff67506b4c8f4f547e3a7521ca16e8e93918a262de637095e6af820590fe22732675474330c006ec9142e7126d9914e_640.jpg"
        ],
        "industry": [
            "https://pixabay.com/get/g354bfcd0b17c0d57c934e40df21335154a9c2acdbaf74bc7060a0b7d6b39beee3b6bbd11ddb33bf129668dfcaafb38a27a24e60b6f9fbbec8741f0e4432d12c8_640.jpg"
        ],
        "air": [
            "https://pixabay.com/get/gd9a224e48b572b0b85dd1b51a1572111269b0c5d975d17fa5249de5e8843261657054168aaacf87973bd57e7f5277613bf9acf50674c7c4e0fe4fe3dfaaf9403_640.jpg"
        ],
        "solutions": [
            "https://pixabay.com/get/g1b10f4570c1c95e2d14380bf730ac9afd4a790c200c579bf637b20e3623372ce74786ecb666191f925c40955932ea8384bc6418fbe7f5db26650fca264358fe6_640.jpg"
        ]
    }
}

```

## Definitions

### Creative
Name | Type | Description |
| :--- | :--- | :--- |
title |	String	|Suggested| title for the creative
description	|String 	|Suggested creative for the creative
keywords	|String[]| 	Keywords extracted from the landing page
images	|String[]|	Suggested images for the creative


There are many reasons to use the Gophish API. The most common use case is to gather report information for a given campaign, so that you can build custom reports in software you're most familiar with, such as Excel or Numbers.

However, automating the creation of campaigns and campaign attributes such as templates, landing pages, and more provides the ability to create a fully automated phishing simulation program. This would allow campaigns to be run throughout the year automatically. This also allows the Gophish administrator to be included in the campaigns, since they wouldn't know exactly which day it would start!

## Authorization

All API requests require the use of a generated API key. You can find your API key, or generate a new one, by navigating to the /settings endpoint, or clicking the “Settings” sidebar item.

To authenticate an API request, you should provide your API key in the `Authorization` header.

Alternatively, you may append the `api_key=[API_KEY]` as a GET parameter to authorize yourself to the API. But note that this is likely to leave traces in things like your history, if accessing the API through a browser.

```http
GET /api/campaigns/?api_key=12345678901234567890123456789012
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. Your Gophish API key |

## Responses

Many API endpoints return the JSON representation of the resources created or edited. However, if an invalid request is submitted, or some other error occurs, Gophish returns a JSON response in the following format:

```javascript
{
  "message" : string,
  "success" : bool,
  "data"    : string
}
```

The `message` attribute contains a message commonly used to indicate errors or, in the case of deleting a resource, success that the resource was properly deleted.

The `success` attribute describes if the transaction was successful or not.

The `data` attribute contains any other metadata associated with the response. This will be an escaped string containing JSON data.

## Status Codes

Gophish returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

