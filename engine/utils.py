import sys
from urllib.parse import urlparse


def show_banner(target: str, mode: str, version: str):
    banner = r"""
 █████╗ ██████╗ ██████╗ ██╗ ██╗███████╗ 
██╔══██╗██╔══██╗██╔════╝ ██║ ██║██╔════╝ 
███████║██████╔╝██║ ███╗██║ ██║███████╗ 
██╔══██║██╔══██╗██║ ██║██║ ██║╚════██║ 
██║ ██║ ██║  ██║╚██████╔╝╚██████╔╝███████║ 
╚═╝ ╚═╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ 

    Automatic Parameter Discovery Engine
    """

    print(banner)
    print(f"    Version : {version}")
    print(f"    Target  : {target}")
    print(f"    Mode    : {mode}")
    print("-" * 55)


def validate_url(url: str):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format. Use http:// or https://")


def normalize_url(url: str) -> str:
    return url.rstrip("/")
