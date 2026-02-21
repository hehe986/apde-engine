import hashlib
from typing import Dict, Any


class ResponseAnalyzer:
    """
    Responsible for analyzing HTTP responses
    and detecting behavioral differences.
    """

    @staticmethod
    def fingerprint(response) -> str:
        """
        Generate stable fingerprint using raw bytes.
        """
        if not response:
            return ""

        return hashlib.md5(response.content).hexdigest()

    @staticmethod
    def compare(baseline, new) -> Dict[str, Any]:
        """
        Compare baseline and new response.
        Returns structured analysis result.
        """

        if not baseline or not new:
            return {"error": "Invalid response comparison"}

        result = {
            "status_changed": baseline.status_code != new.status_code,
            "length_changed": len(baseline.content) != len(new.content),
            "fingerprint_changed": (
                ResponseAnalyzer.fingerprint(baseline)
                != ResponseAnalyzer.fingerprint(new)
            ),
            "reflection_detected": False,
            "rate_limited": new.status_code == 429,
        }

        return result

    @staticmethod
    def detect_reflection(response, payload: str) -> bool:
        """
        Detect if payload is reflected in response body.
        """
        if not response or not payload:
            return False

        return payload in response.text
