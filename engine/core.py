import requests
from typing import Optional, Dict


class RequestEngine:

    def __init__(
        self,
        timeout: int = 10,
        proxy: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True
    ):
        self.timeout = timeout
        self.proxy = proxy
        self.verify_ssl = verify_ssl

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "APDE/0.1 (Automatic Parameter Discovery Engine)"
        })

    def send(self, method: str, url: str, **kwargs):
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                timeout=self.timeout,
                proxies=self.proxy,
                verify=self.verify_ssl,
                allow_redirects=True,
                **kwargs
            )
            return response
        except requests.RequestException:
            return None


class Injector:

    TEST_VALUE = "apde_test"

    @staticmethod
    def build_get(param: str):
        return {param: Injector.TEST_VALUE}

    @staticmethod
    def build_post(param: str):
        return {param: Injector.TEST_VALUE}

    @staticmethod
    def build_json(param: str):
        return {param: Injector.TEST_VALUE}

    @staticmethod
    def build_header(param: str):
        return {param: Injector.TEST_VALUE}
