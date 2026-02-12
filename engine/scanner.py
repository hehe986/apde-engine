from .core import RequestEngine, Injector, Analyzer


class APDEScanner:

    def __init__(self, target: str, timeout=10, proxy=None):
        self.target = target
        self.engine = RequestEngine(timeout=timeout, proxy=proxy)
        self.injector = Injector()
        self.analyzer = Analyzer()

    def baseline(self):
        return self.engine.send("GET", self.target)

    def scan_get(self, wordlist: list):
        findings = []
        base = self.baseline()

        for param in wordlist:
            response = self.engine.send(
                "GET",
                self.target,
                params=self.injector.build_get(param)
            )

            result = self.analyzer.compare(base, response)

            if self.analyzer.is_interesting(result):
                findings.append({
                    "method": "GET",
                    "parameter": param,
                    "analysis": result
                })

        return findings

    def scan_post(self, wordlist: list):
        findings = []
        base = self.baseline()

        for param in wordlist:
            response = self.engine.send(
                "POST",
                self.target,
                data=self.injector.build_post(param)
            )

            result = self.analyzer.compare(base, response)

            if self.analyzer.is_interesting(result):
                findings.append({
                    "method": "POST",
                    "parameter": param,
                    "analysis": result
                })

        return findings

    def scan_json(self, wordlist: list):
        findings = []
        base = self.baseline()

        for param in wordlist:
            response = self.engine.send(
                "POST",
                self.target,
                json=self.injector.build_json(param)
            )

            result = self.analyzer.compare(base, response)

            if self.analyzer.is_interesting(result):
                findings.append({
                    "method": "JSON",
                    "parameter": param,
                    "analysis": result
                })

        return findings

    def scan_header(self, wordlist: list):
        findings = []
        base = self.baseline()

        for param in wordlist:
            headers = self.injector.build_header(param)
            response = self.engine.send(
                "GET",
                self.target,
                headers=headers
            )

            result = self.analyzer.compare(base, response)

            if self.analyzer.is_interesting(result):
                findings.append({
                    "method": "HEADER",
                    "parameter": param,
                    "analysis": result
                })

        return findings
