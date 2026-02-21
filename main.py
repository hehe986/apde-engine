#!/usr/bin/env python3
"""
APDE - Automatic Parameter Discovery Engine
Main CLI Entry Point
"""

import argparse
import sys
from pathlib import Path

from engine import APDEScanner, ScanConfig
from engine.reporting import Reporter
from engine.utils import show_banner, validate_url, normalize_url


# ===============================
# Argument Parsing
# ===============================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="APDE - Automatic Parameter Discovery Engine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Target URL (e.g., https://example.com)"
    )

    parser.add_argument(
        "--wordlist",
        default="wordlists/common.txt",
        help="Path to wordlist file"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Save report to JSON file"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP request timeout (seconds)"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests (seconds)"
    )

    return parser.parse_args()


# ===============================
# Main
# ===============================

def load_wordlist(path: str):
    file_path = Path(path)

    if not file_path.exists():
        print(f"[!] Wordlist not found: {path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    args = parse_arguments()

    # URL Validation
    try:
        validate_url(args.url)
    except ValueError as e:
        print(f"[!] {e}")
        sys.exit(1)

    target = normalize_url(args.url)

    # Banner
    show_banner(
        target=target,
        mode="Standard",
        version="v1.0"
    )

    print(f"[+] Target: {target}")
    print(f"[+] Wordlist: {args.wordlist}")
    print(f"[+] Timeout: {args.timeout}")
    print(f"[+] Delay: {args.delay}")
    print("-" * 50)

    # Load wordlist
    wordlist = load_wordlist(args.wordlist)

    # Config object (new architecture)
    config = ScanConfig(
        target=target,
        timeout=args.timeout,
        delay=args.delay
    )

    # Scanner
    scanner = APDEScanner(config)

    # Run scans (you can expand modes later)
    results = scanner.scan_get(wordlist)

    # Reporting
    reporter = Reporter(results)

    reporter.print_summary()

    if args.output:
        reporter.save_json(args.output)
        print(f"[+] Report saved to {args.output}")


if __name__ == "__main__":
    main()
