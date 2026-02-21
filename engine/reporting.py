import json
import os
from .utils import timestamp


class Reporter:

    def __init__(self, results):
        self.results = results

    def console(self):
        if not self.results:
            print("[+] No interesting parameter behavior found.")
            return

        print("[+] Potential Findings:\n")

        for item in self.results:
            print(f"[{item['type']}] Parameter: {item.get('parameter')}")
            print(f"  Status Changed : {item['analysis']['status_changed']}")
            print(f"  Length Changed : {item['analysis']['length_changed']}")
            print(f"  Fingerprint    : {item['analysis']['fingerprint_changed']}")
            print(f"  Reflection     : {item.get('reflection')}")
            print()

    def save_json(self, output_dir="reports"):
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/apde_{timestamp()}.json"

        report = {
            "generated_at": timestamp(),
            "total_findings": len(self.results),
            "findings": self.results
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        return filename
