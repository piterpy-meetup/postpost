from io import BytesIO
from typing import IO

import requests


def download_media(url: str) -> IO[bytes]:
    """
    Downloads media by the given link and returns IO with it.
    """
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    reader = BytesIO(response.content)
    reader.name = url.split('/')[-1]
    return reader
