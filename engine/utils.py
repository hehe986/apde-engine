import datetime
from urllib.parse import urlparse


BANNER = r"""
   █████╗ ██████╗  ██████╗ ██╗   ██╗███████╗
  ██╔══██╗██╔══██╗██╔════╝ ██║   ██║██╔════╝
  ███████║██████╔╝██║  ███╗██║   ██║███████╗
  ██╔══██║██╔═══╝ ██║   ██║██║   ██║╚════██║
  ██║  ██║██║     ╚██████╔╝╚██████╔╝███████║
  ╚═╝  ╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚══════╝
"""


def show_banner(target: str, mode: str, version: str = "v0.1"):
    print(BANNER)
    print("┌────────────────────────────────────────────────┐")
    print("│ ARGUS - Parameter Intelligence Scanner        │")
    print("│ Powered by Automatic Parameter Discovery Eng. │")
    print(f"│ Version : {version:<38}│")
    print("│ Author  : H1lm1.exe                            │")
    print(f"│ Mode    : {mode:<38}│")
    print(f"│ Target  : {target:<38}│")
    print("└────────────────────────────────────────────────┘")
    print()


def validate_url(url: str):
    parsed = urlparse(url)

    if parsed.scheme not in ["http", "https"]:
        raise ValueError("Target must start with http:// or https://")

    if not parsed.netloc:
        raise ValueError("Invalid target URL")


def normalize_url(url: str):
    return url.rstrip("/")


def timestamp():
    return datetime.datetime.utcnow().isoformat()
