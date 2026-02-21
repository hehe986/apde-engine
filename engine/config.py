from dataclasses import dataclass
from typing import Optional


@dataclass
class ScanConfig:
    """
    Central configuration object.
    """

    target: str
    delay: float = 0.5
    timeout: int = 10
    verify_ssl: bool = True
    proxy: Optional[str] = None
    stop_on_rate_limit: bool = True
    max_rate_limit_hits: int = 3

    def validate(self):
        if not self.target.startswith(("http://", "https://")):
            raise ValueError("Target must start with http:// or https://")
