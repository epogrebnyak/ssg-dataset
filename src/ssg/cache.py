# TODO: Need stable location for the file.
# The cache file may appear in different folders for example and tests.
# Also need some machinery to delete this cache file.

import os

import requests_cache  # type: ignore
from dotenv import load_dotenv

__all__ = ["has_token"]


requests_cache.install_cache("cache_1")
load_dotenv(".config.env")
GH_USER = os.getenv("GH_USER", "")
GH_TOKEN = os.getenv("GH_TOKEN", "")


def has_token():
    """Reveal if token is available."""
    if GH_TOKEN:
        print(f"Token for {GH_USER} is found.")
    else:
        print(f"No token found for {GH_USER}.")
