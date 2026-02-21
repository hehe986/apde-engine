import time
from typing import List, Dict

from .analyzer import ResponseAnalyzer
from .http_client import HTTPClient
from .config import ScanConfig


class APDEScanner:
    """
    Main scanning orchestrator.
    Responsible for:
    - baseline generation
    - payload injection
    - calling analyzer
    - respecting config rules
    """

    def __init__(self, config: ScanConfig):
        config.validate()

        self.config = config
        self.client = HTTPClient(
            timeout=config.timeout,
            verify_ssl=config.verify_ssl,
            proxy=config.proxy,
        )

        self.analyzer = ResponseAnalyzer()
        self.rate_limit_hits = 0

    # ===============================
    # Baseline Handling
    # ===============================

    def baseline(self, mode: str = "GET"):
        if mode == "POST":
            return self.client.send("POST", self.config.target, data={})

        elif mode == "JSON":
            return self.client.send("POST", self.config.target, json={})

        else:
            return self.client.send("GET", self.config.target)

    # ===============================
    # Core Scan Logic
    # ===============================

    def scan_get(self, wordlist: List[str]) -> List[Dict]:
        print("[*] Starting GET parameter scan...")

        base = self.baseline("GET")
        if not base:
            print("[-] Failed to obtain baseline.")
            return []

        findings = []

        for param in wordlist:
            time.sleep(self.config.delay)

            response = self.client.send(
                "GET",
                self.config.target,
                params={param: "apde_test"},
            )

            if not response:
                continue

            analysis = self.analyzer.compare(base, response)

            if analysis.get("rate_limited"):
                self.rate_limit_hits += 1
                print("[!] Rate limit detected")

                if (
                    self.config.stop_on_rate_limit
                    and self.rate_limit_hits >= self.config.max_rate_limit_hits
                ):
                    print("[!] Stopping scan due to repeated rate limiting.")
                    break

            if (
                analysis["status_changed"]
                or analysis["length_changed"]
                or analysis["fingerprint_changed"]
            ):
                findings.append(
                    {
                        "type": "GET",
                        "parameter": param,
                        "analysis": analysis,
                        "reflection": self.analyzer.detect_reflection(
                            response, "apde_test"
                        ),
                    }
                )

        return findings

    # ===============================
    # POST Scan
    # ===============================

    def scan_post(self, wordlist: List[str]) -> List[Dict]:
        print("[*] Starting POST parameter scan...")

        base = self.baseline("POST")
        if not base:
            print("[-] Failed to obtain baseline.")
            return []

        findings = []

        for param in wordlist:
            time.sleep(self.config.delay)

            response = self.client.send(
                "POST",
                self.config.target,
                data={param: "apde_test"},
            )

            if not response:
                continue

            analysis = self.analyzer.compare(base, response)

            if analysis.get("rate_limited"):
                self.rate_limit_hits += 1
                print("[!] Rate limit detected")

                if (
                    self.config.stop_on_rate_limit
                    and self.rate_limit_hits >= self.config.max_rate_limit_hits
                ):
                    print("[!] Stopping scan due to repeated rate limiting.")
                    break

            if (
                analysis["status_changed"]
                or analysis["length_changed"]
                or analysis["fingerprint_changed"]
            ):
                findings.append(
                    {
                        "type": "POST",
                        "parameter": param,
                        "analysis": analysis,
                        "reflection": self.analyzer.detect_reflection(
                            response, "apde_test"
                        ),
                    }
                )

        return findings

    # ===============================
    # JSON Scan
    # ===============================

    def scan_json(self, wordlist: List[str]) -> List[Dict]:
        print("[*] Starting JSON parameter scan...")

        base = self.baseline("JSON")
        if not base:
            print("[-] Failed to obtain baseline.")
            return []

        findings = []

        for param in wordlist:
            time.sleep(self.config.delay)

            response = self.client.send(
                "POST",
                self.config.target,
                json={param: "apde_test"},
            )

            if not response:
                continue

            analysis = self.analyzer.compare(base, response)

            if analysis.get("rate_limited"):
                self.rate_limit_hits += 1
                print("[!] Rate limit detected")

                if (
                    self.config.stop_on_rate_limit
                    and self.rate_limit_hits >= self.config.max_rate_limit_hits
                ):
                    print("[!] Stopping scan due to repeated rate limiting.")
                    break

            if (
                analysis["status_changed"]
                or analysis["length_changed"]
                or analysis["fingerprint_changed"]
            ):
                findings.append(
                    {
                        "type": "JSON",
                        "parameter": param,
                        "analysis": analysis,
                        "reflection": self.analyzer.detect_reflection(
                            response, "apde_test"
                        ),
                    }
                )

        return findings

    # ===============================
    # HEADER Scan
    # ===============================

    def scan_header(self, wordlist: List[str]) -> List[Dict]:
        print("[*] Starting Header injection scan...")

        base = self.baseline("GET")
        if not base:
            print("[-] Failed to obtain baseline.")
            return []

        findings = []

        for header in wordlist:
            time.sleep(self.config.delay)

            custom_headers = self.client.session.headers.copy()
            custom_headers.update({header: "apde_test"})

            response = self.client.send(
                "GET",
                self.config.target,
                headers=custom_headers,
            )

            if not response:
                continue

            analysis = self.analyzer.compare(base, response)

            if analysis.get("rate_limited"):
                self.rate_limit_hits += 1
                print("[!] Rate limit detected")

                if (
                    self.config.stop_on_rate_limit
                    and self.rate_limit_hits >= self.config.max_rate_limit_hits
                ):
                    print("[!] Stopping scan due to repeated rate limiting.")
                    break

            if (
                analysis["status_changed"]
                or analysis["length_changed"]
                or analysis["fingerprint_changed"]
            ):
                findings.append(
                    {
                        "type": "HEADER",
                        "header": header,
                        "analysis": analysis,
                    }
                )

        return findings


