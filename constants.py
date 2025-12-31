from enum import Enum
from HyperUserAgent import HyperUA


class API(Enum):
    PROTOCOL = "https://"
    BASE_URL = "cooltext.com"
    RENDER_ENDPOINT = "/Render"
    CHANGE_ENDPOINT = "/PostChange"
    RENDER_LOCATION = "renderLocation"


class Requests(Enum):
    ACCEPT = "*/*"
    ACCEPT_LANGUAGE = "en-US,en;q=0.7"
    CONTENT_TYPE = "application/x-www-form-urlencoded; charset=UTF-8"
    ORIGIN = API.PROTOCOL.value + API.BASE_URL.value
    PRIORITY = "u=1, i"
    SEC_CH_UA = '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"'
    SEC_CH_UA_MOBILE = "?0"
    SEC_CH_UA_PLATFORM = '"Windows"'
    SEC_FETCH_DEST = "empty"
    SEC_FETCH_MODE = "cors"
    SEC_FETCH_SITE = "same-origin"
    SEC_GPC = "1"
    X_REQUESTED_WITH = "XMLHttpRequest"
    USER_AGENT = str(HyperUA().chrome)

    @classmethod
    def header(cls, Referer) -> dict:
        header = {
            member.name.replace("_", "-").title(): str(member.value) for member in cls
        }
        header["Referer"] = Referer
        return header


class DefaultValues(Enum):
    NONE_STR = ""
    BACKGROUND_COLOR = "#FFFFFF"
    FILE_FORMAT = "6"
    FONT_SIZE = "120"
    TEXT = "CoolText"


class ConfigFile(Enum):
    LOGO_ID_FILE = "./logo-id.json"
    OPEN_TYPE = "r"
    LOGO_LINK = "LogoLink"
    DEFAULTS = "defaults"


class ExceptionMessages(Enum):
    HTTP_REQUEST_FAILED = "HTTP request to CoolText failed: %s"
    JSON_DECODE_FAILED = "Failed to decode JSON response from CoolText"
    UNEXPECTED_RESPONSE = "Unexpected CoolText response, missing '%s': %s"
