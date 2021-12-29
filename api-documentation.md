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

