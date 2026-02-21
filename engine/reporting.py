import json
import os
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

    def save_json(self, findings: list, output_dir="reports"):
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/apde_{timestamp()}.json"

        report = {
            "generated_at": timestamp(),
            "total_findings": len(findings),
            "findings": findings
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        return filename
