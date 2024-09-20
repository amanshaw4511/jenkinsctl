from urllib.parse import urljoin

import requests
import logging

logger = logging.getLogger(__name__)

class Session(requests.Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def request(
            self,
            method,
            url,
            **kwargs
    ):
        joined_url = urljoin(self.base_url, url)
        # logger.debug(joined_url)
        return super().request(method, joined_url, **kwargs)

