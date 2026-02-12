import requests
import hashlib
from typing import Optional, Dict, Any


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


class Analyzer:

    LENGTH_THRESHOLD = 40

    @staticmethod
    def fingerprint(response):
        if not response:
            return None
        return hashlib.md5(response.text.encode()).hexdigest()

    @staticmethod
    def compare(base, new):
        if not base or not new:
            return None

        length_diff = abs(len(base.text) - len(new.text))

        return {
            "status_changed": base.status_code != new.status_code,
            "length_diff": length_diff,
            "redirected": len(new.history) > 0,
            "reflected": Injector.TEST_VALUE in new.text,
            "fingerprint_changed":
                Analyzer.fingerprint(base) != Analyzer.fingerprint(new)
        }

    @staticmethod
    def is_interesting(result):
        if not result:
            return False

        if result["status_changed"]:
            return True
        if result["length_diff"] > Analyzer.LENGTH_THRESHOLD:
            return True
        if result["redirected"]:
            return True
        if result["reflected"]:
            return True
        if result["fingerprint_changed"]:
            return True

        return False
