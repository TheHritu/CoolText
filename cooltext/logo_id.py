# This file was used to generate logo_id.json,

# This has nothing to do with the main module functionality.

# It scrapes the cooltext.com website to get LogoIDs and their default values.

import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = "https://cooltext.com/"
INPUTS_IDS = [
    "LogoID",
    "Text",
    "FontSize",
    "FileFormat",
    "BackgroundColor_color",
    "Color1_color",
    "Color2_color",
    "Color3_color",
    "Boolean1",
    "Boolean2",
    "Boolean3",
    "Integer1",
    "Integer2",
    "Integer3",
    "Integer4",
    "Integer5",
    "Integer6",
    "Integer7",
    "Integer8",
    "Integer9",
    "Integer10",
    "Integer11",
    "Integer12",
    "Integer13",
    "Integer14_color",
]


def get_headers():
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://cooltext.com",
        "priority": "u=1, i",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": str(UserAgent(os=["Windows"]).chrome),
        "x-requested-with": "XMLHttpRequest",
    }


def get_logo_gallery(headers):
    """Fetch the main page and return the LogoGallery div."""
    response = requests.get(URL, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")
    return soup.find("div", {"class": "LogoGallery"})


def get_logo_defaults(logo_url, headers):
    """Fetch a logo's page and return its metadata and default input values."""
    response = requests.get(logo_url, headers=headers).content
    soup = BeautifulSoup(response, "html.parser")

    logoid = soup.find("input", {"id": "LogoID"})["value"]
    preview_image = soup.find("img", {"id": "PreviewImage"})["src"]

    defaults = {}
    for input_id in INPUTS_IDS[1:]:
        input_element = soup.find("input", {"id": input_id})
        if input_element:
            if "disabled" in input_element.attrs:
                pass
            elif "value" in input_element.attrs and input_element.get("value") != "":
                defaults[input_id] = input_element["value"]
            elif input_element.has_attr("checked"):
                defaults[input_id] = "on"
        else:
            select = soup.find("select", {"id": input_id})
            if select:
                option = select.find("option", selected=True)
                if option and "value" in option.attrs:
                    defaults[input_id] = option["value"]

    return logoid, preview_image, defaults


def scrape_logos():
    """Main scraping logic. Returns the full logo data dict."""
    headers = get_headers()
    logo_gallery = get_logo_gallery(headers)
    data = {}

    for item in logo_gallery:
        try:
            a_link = item.find("a", {"class": "LogoLink"})["href"]
            logo_url = "https://cooltext.com" + a_link

            logoid, preview_image, defaults = get_logo_defaults(logo_url, headers)
            data[logoid] = {
                "LogoLink": logo_url,
                "PreviewImage": preview_image,
                "defaults": defaults,
            }
        except Exception as e:
            print(item)
            print(e)

    return data
