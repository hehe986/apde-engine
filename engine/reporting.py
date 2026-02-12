import json
from .utils import timestamp


class Reporter:

    def console(self, findings: list):
        if not findings:
            print("[+] No interesting parameter behavior found.")
            return

        print("[+] Potential Findings:\n")

        for item in findings:
            print(f"[{item['method']}] Parameter: {item['parameter']}")
            print(f"  Status Changed : {item['analysis']['status_changed']}")
            print(f"  Length Diff    : {item['analysis']['length_diff']}")
            print(f"  Redirected     : {item['analysis']['redirected']}")
            print(f"  Reflected      : {item['analysis']['reflected']}")
            print()

    def save_json(self, findings: list, output_file: str):
        report = {
            "generated_at": timestamp(),
            "total_findings": len(findings),
            "findings": findings
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)

    def score(self, findings: list):
        score = 0
        for item in findings:
            if item["analysis"]["status_changed"]:
                score += 3
            if item["analysis"]["reflected"]:
                score += 3
            if item["analysis"]["length_diff"] > 100:
                score += 2
            if item["analysis"]["redirected"]:
                score += 1
        return score
