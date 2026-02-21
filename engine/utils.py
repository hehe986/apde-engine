import sys
from urllib.parse import urlparse
from datetime import datetime

BANNER = r"""
 █████╗ ██████╗  ██████╗ ██╗   ██╗███████╗
██╔══██╗██╔══██╗██╔════╝ ██║   ██║██╔════╝
███████║██████╔╝██║  ███╗██║   ██║███████╗
██╔══██║██╔══██╗██║   ██║██║   ██║╚════██║
██║  ██║██║  ██║╚██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝
"""


def show_banner(target: str, mode: str, version: str = "v1.0"):
    print(BANNER)
    print("┌──────────────────────────────────────────────────────┐")
    print("│ APDE - Automatic Parameter Discovery Engine         │")
    print("│ Intelligent Parameter Behavior Scanner              │")
    print("│ Author  : H1lm1.exe                                 │")
    print("│ Codename: ARGUS                                     │")
    print(f"│ Version : {version:<42}│")
    print(f"│ Mode    : {mode:<42}│")
    print(f"│ Target  : {target:<42}│")
    print("└──────────────────────────────────────────────────────┘")
    print()


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def validate_url(url: str):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format. Use http:// or https://")


def normalize_url(url: str) -> str:
    return url.rstrip("/")
