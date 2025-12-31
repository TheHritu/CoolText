import json
import logging
import requests
from typing import Optional
from urllib.parse import quote
from pydantic import BaseModel
from constants import DefaultValues, Requests, ConfigFile, API, ExceptionMessages


class PostChangeConfigOptions(BaseModel):
    LogoID: str
    Text: str = DefaultValues.TEXT.value
    FontSize: str = DefaultValues.FONT_SIZE.value
    FileFormat: str = DefaultValues.FILE_FORMAT.value
    BackgroundColor_color: str = DefaultValues.BACKGROUND_COLOR.value
    Color1_color: Optional[str] = None
    Color2_color: Optional[str] = None
    Boolean1: Optional[str] = None
    Boolean2: Optional[str] = None
    Boolean3: Optional[str] = None
    Integer1: Optional[str] = None
    Integer2: Optional[str] = None
    Integer3: Optional[str] = None
    Integer4: Optional[str] = None
    Integer5: Optional[str] = None
    Integer6: Optional[str] = None
    Integer7: Optional[str] = None
    Integer8: Optional[str] = None
    Integer9: Optional[str] = None
    Integer10: Optional[str] = None
    Integer11: Optional[str] = None
    Integer12: Optional[str] = None
    Integer13: Optional[str] = None
    Integer14_color: Optional[str] = None


class CoolText:
    def __init__(self, config: PostChangeConfigOptions):
        self.config = config

    def get_payload(self) -> dict:
        return self.config.model_dump(exclude_none=True)

    def get_defaults(self) -> dict:
        link_ID_file = json.loads(
            open(ConfigFile.LOGO_ID_FILE.value, ConfigFile.OPEN_TYPE.value).read()
        )
        return link_ID_file[self.config.LogoID][ConfigFile.DEFAULTS.value]

    def get_link(self) -> str:
        link_ID_file = json.loads(
            open(ConfigFile.LOGO_ID_FILE.value, ConfigFile.OPEN_TYPE.value).read()
        )
        return link_ID_file[self.config.LogoID][ConfigFile.LOGO_LINK.value]

    def get_headers(self) -> dict:
        return Requests.header(Referer=self.get_link())

    def create(self) -> Optional[str]:
        logger = logging.getLogger(__name__)
        url = API.PROTOCOL.value + API.BASE_URL.value + API.CHANGE_ENDPOINT.value
        payload = {**self.get_payload(), **self.get_defaults()}
        headers = self.get_headers()
        try:
            with requests.Session() as s:
                resp_get = s.get(self.get_link(), headers=headers, timeout=10)
                resp_get.raise_for_status()
                resp_post = s.post(url, data=payload, headers=headers, timeout=10)
                resp_post.raise_for_status()
                data = resp_post.json()
        except requests.exceptions.RequestException as exc:
            logger.exception(ExceptionMessages.HTTP_REQUEST_FAILED.value, exc)
            return None
        except ValueError:
            logger.exception(ExceptionMessages.JSON_DECODE_FAILED.value)
            return None
        render_key = API.RENDER_LOCATION.value
        if render_key not in data:
            logger.warning(
                ExceptionMessages.UNEXPECTED_RESPONSE.value, render_key, data
            )
            return None
        render_path = str(data[render_key]).replace(
            API.PROTOCOL.value, DefaultValues.NONE_STR.value
        )
        return API.PROTOCOL.value + quote(render_path)
