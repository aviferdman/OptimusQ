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

### ImagePropertiesPixable
Parameter | Type | Description |
| :--- | :--- | :--- |
q |	str |	A URL encoded search term. If omitted, all images are returned. This value may not exceed 100 characters. Example: "yellow+flower"
lang | str | Language code of the language to be searched in. Accepted values: cs, da, de, en, es, fr, id, it, hu, nl, no, pl, pt, ro, sk, fi, sv, tr, vi, th, bg, ru, el, ja, ko, zh. Default: "en"
id | str | Retrieve individual images by ID.
image_type | str | Filter results by image type.
Accepted values: "all", "photo", "illustration", "vector". Default: "all"
orientation | str |	Whether an image is wider than it is tall, or taller than it is wide. Accepted values: "all", "horizontal", "vertical" Default: "all"
category | str | Filter results by category. Accepted values: backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music min_width	int	Minimum image width. Default: "0"
min_height | int | Minimum image height. Default: "0"
colors | str | Filter images by color properties. A comma separated list of values may be used to select multiple properties. Accepted values: "grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown"
editors_choice | bool |	Select images that have received an Editor's Choice award. Accepted values: "true", "false". Default: "false"
safesearch	| bool | A flag indicating that only images suitable for all ages should be returned. Accepted values: "true", "false". Default: "false"
order |	str |	How the results should be ordered. Accepted values: "popular", "latest". Default: "popular"
page | int | Returned search results are paginated. Use this parameter to select the page number. Default: 1
per_page | int | Determine the number of results per page. Accepted values: 3 - 200 Default: 20
callback | string |	JSONP callback function name
pretty | bool |	Indent JSON output. This option should not be used in production. Accepted values: "true", "false". Default: "false"

