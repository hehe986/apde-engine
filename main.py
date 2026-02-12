#!/usr/bin/env python3
"""
APDE - Automatic Parameter Discovery Engine
Main CLI Entry Point
"""

import argparse
import sys
from engine import APDEScanner, Reporter
from engine.utils import show_banner, validate_url, normalize_url


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
        "--threads",
        type=int,
        default=5,
        help="Number of concurrent threads"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        validate_url(args.url)
    except ValueError as e:
        print(f"[!] {e}")
        sys.exit(1)

    target = normalize_url(args.url)

    show_banner(
        target=target,
        mode="Standard",
        version="v0.1"
    )

    print(f"[+] Target: {target}")
    print(f"[+] Wordlist: {args.wordlist}")
    print(f"[+] Threads: {args.threads}")
    print(f"[+] Timeout: {args.timeout}")
    print("-" * 50)

    scanner = APDEScanner(
        target=target,
        wordlist_path=args.wordlist,
        timeout=args.timeout,
        threads=args.threads
    )

    results = scanner.run()

    reporter = Reporter(results)

    reporter.print_summary()

    if args.output:
        reporter.save_json(args.output)
        print(f"[+] Report saved to {args.output}")

if __name__ == "__main__":
    main()
