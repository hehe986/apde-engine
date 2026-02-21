import requests
from typing import Optional, Dict, Any


class HTTPClient:
    """
    Wrapper around requests.Session
    Handles connection reuse, proxies, headers, SSL, timeout.
    """

    def __init__(
        self,
        timeout: int = 10,
        verify_ssl: bool = True,
        proxy: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
    ):
        self.session = requests.Session()
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if default_headers:
            self.session.headers.update(default_headers)
        else:
            self.session.headers.update(
                {
                    "User-Agent": "APDE Scanner/1.0"
                }
            )

        if proxy:
            self.session.proxies.update(
                {
                    "http": proxy,
                    "https": proxy,
                }
            )

    def send(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Send HTTP request safely.
        """

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=True,
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"[HTTP ERROR] {e}")
            return None
