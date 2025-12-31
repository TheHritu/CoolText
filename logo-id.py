# This file was used to generate logo-id.json,
# This has nothing to do with the main module functionality.
# It scrapes the cooltext.com website to get LogoIDs and their default values.

import requests
from bs4 import BeautifulSoup
from HyperUserAgent import HyperUA

url = "https://cooltext.com/"
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://cooltext.com",
    "priority": "u=1, i",
    "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": str(HyperUA().chrome),
    "x-requested-with": "XMLHttpRequest",
}
rez = requests.get(url, headers=headers).content
soup1 = BeautifulSoup(rez, "html.parser")
LogoGallery = soup1.find("div", {"class": "LogoGallery"})
data = {}
inputs_ids = [
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
for i in LogoGallery:
    try:
        a_link = i.find("a", {"class": "LogoLink"})["href"]
        LogoLink = "https://cooltext.com" + a_link
        riz = requests.get(LogoLink, headers=headers).content
        soup2 = BeautifulSoup(riz, "html.parser")
        PreviewImage = soup2.find("img", {"id": "PreviewImage"})["src"]
        logoid = soup2.find("input", {"id": "LogoID"})["value"]
        data[logoid] = {}
        data[logoid]["LogoLink"] = LogoLink
        data[logoid]["PreviewImage"] = PreviewImage
        data[logoid]["defaults"] = {}
        for input_id in inputs_ids[1:]:
            input_element = soup2.find("input", {"id": input_id})
            if input_element:
                if "disabled" in input_element.attrs:
                    pass
                elif (
                    "value" in input_element.attrs and input_element.get("value") != ""
                ):
                    data[logoid]["defaults"][input_id] = input_element["value"]
                elif input_element.has_attr("checked"):
                    data[logoid]["defaults"][input_id] = "on"
            else:
                select = soup2.find("select", {"id": input_id})
                if select:
                    option = select.find("option", selected=True)
                    if option and "value" in option.attrs:
                        data[logoid]["defaults"][input_id] = option["value"]
    except Exception as e:
        print(i)
        print(e)
        continue
import json

with open("logo-id.json", "w") as f:
    json.dump(data, f, indent=4)
