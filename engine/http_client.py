import requests
import certifi
import urllib3
from typing import Optional, Dict, Any

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

        # Jika verify_ssl True, gunakan certifi; kalau False, tetap False
        self.verify_ssl = certifi.where() if verify_ssl else False

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
        Send HTTP request safely with certifi SSL bundle.
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

        except requests.exceptions.SSLError as ssl_err:
            print(f"[SSL WARNING] {ssl_err}")
            print("[*] Retrying without SSL verification...")

            try:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                    timeout=self.timeout,
                    verify=False,  # fallback, ignore SSL
                    allow_redirects=True,
                )
                return response

            except requests.exceptions.RequestException as e:
                print(f"[HTTP ERROR] {e}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"[HTTP ERROR] {e}")
            return None
