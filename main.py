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
# Utilities
# ===============================

def load_wordlist(path: str):
    file_path = Path(path)

    if not file_path.exists():
        print(f"[!] Wordlist not found: {path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    if not words:
        print("[!] Wordlist is empty.")
        sys.exit(1)

    return words


# ===============================
# Main Execution
# ===============================

def main():
    args = parse_arguments()

    # Validate URL
    try:
        validate_url(args.url)
    except ValueError as e:
        print(f"[!] {e}")
        sys.exit(1)

    target = normalize_url(args.url)

    # Show ASCII Banner
    show_banner(
        target=target,
        mode="GET",
        version="v1.0"
    )

    print(f"[+] Wordlist : {args.wordlist}")
    print(f"[+] Timeout  : {args.timeout}s")
    print(f"[+] Delay    : {args.delay}s")
    print("-" * 55)

    # Load wordlist
    wordlist = load_wordlist(args.wordlist)

    # Build configuration
    config = ScanConfig(
        target=target,
        timeout=args.timeout,
        delay=args.delay
    )

    # Initialize scanner
    scanner = APDEScanner(config)

    # Run scan safely
    try:
        results = scanner.scan_get(wordlist)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit(0)

    # Reporting
    reporter = Reporter(results)
    reporter.console()

    if args.output:
        reporter.save_json(args.output)
        print(f"[+] Report saved to {args.output}")


if __name__ == "__main__":
    main()

