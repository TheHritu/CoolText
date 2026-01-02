import os
import json
import logging
import requests
from typing import Optional
from urllib.parse import quote
from pydantic import BaseModel
from constants import (
    API,
    Extras,
    Requests,
    ConfigFile,
    DefaultValues,
    LoggerMessages,
)


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


class CoolTextResult:
    def __init__(self, url: str, headers: dict, file_format: str):
        self._url = url
        self._headers = headers
        self._file_format = file_format

    def __str__(self) -> str:
        return self._url if self._url else DefaultValues.NONE_STR.value

    def __repr__(self) -> str:
        return Extras.REPR_TEXT.value.format(self._url)

    def __bool__(self) -> bool:
        return bool(self._url)

    def download(
        self, filepath: Optional[str] = None, timeout: int = 30, stream: bool = True
    ) -> Optional[str]:
        logger = logging.getLogger(__name__)

        if not self._url:
            logger.error(LoggerMessages.NO_URL_AVAILABLE.value)
            return None

        try:
            if filepath is None:
                filename = os.path.basename(
                    self._url.split(Extras.TEXT_QUESTION_MARK.value)[0]
                )
                if not filename or Extras.TEXT_DOT.value not in filename:
                    import time

                    timestamp = int(time.time())
                    filename = (
                        Extras.FILENAME_IF_NOT_DOT_IN_FILENAME_EARLIER.value.format(
                            timestamp, self._file_format.lower()
                        )
                    )
                filepath = filename
            if not filepath.lower().endswith(
                Extras.TEXT_DOT.value + str(self._file_format.lower())
            ):
                filepath = (
                    str(os.path.splitext(filepath)[0])
                    + Extras.TEXT_DOT.value
                    + self._file_format.lower()
                )
            logger.info(
                LoggerMessages.DOWNLOADING_FROM.value.format(self._url, filepath)
            )

            if stream:
                response = requests.get(
                    self._url,
                    headers=self._headers,
                    timeout=timeout,
                    stream=True,
                )
                response.raise_for_status()
                with open(filepath, Extras.OPEN_AS_WRITE_BINARY.value) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            else:
                response = requests.get(
                    self._url, headers=self._headers, timeout=timeout
                )
                response.raise_for_status()
                with open(filepath, Extras.OPEN_AS_WRITE_BINARY.value) as f:
                    f.write(response.content)
            logger.info(LoggerMessages.SUCCESSFULLY_DOWNLOADED.value.format(filepath))
            return filepath
        except requests.exceptions.RequestException as exc:
            logger.exception(LoggerMessages.FAILED_TO_DOWNLOAD.value.format(exc))
            return None
        except IOError as exc:
            logger.exception(LoggerMessages.FAILED_TO_SAVE_FILE.value.format(exc))
            return None
        except Exception as exc:
            logger.exception(LoggerMessages.UNEXPECTED_ERROR.value.format(exc))
            return None


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

    def create(self) -> CoolTextResult:
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
            logger.exception(LoggerMessages.HTTP_REQUEST_FAILED.value, exc)
            return CoolTextResult(
                DefaultValues.NONE_STR.value, {}, DefaultValues.NONE_STR.value
            )
        except ValueError:
            logger.exception(LoggerMessages.JSON_DECODE_FAILED.value)
            return CoolTextResult(
                DefaultValues.NONE_STR.value, {}, DefaultValues.NONE_STR.value
            )

        render_key = API.RENDER_LOCATION.value
        if render_key not in data:
            logger.warning(LoggerMessages.UNEXPECTED_RESPONSE.value, render_key, data)
            return CoolTextResult(
                DefaultValues.NONE_STR.value, {}, DefaultValues.NONE_STR.value
            )

        render_path = str(data[render_key]).replace(
            API.PROTOCOL.value, DefaultValues.NONE_STR.value
        )
        result_url = API.PROTOCOL.value + quote(render_path)
        return CoolTextResult(
            url=result_url, headers=headers, file_format=Extras.FILE_FORMAT.value
        )
