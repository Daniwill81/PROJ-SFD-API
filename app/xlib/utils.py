"""Utils."""


import urllib.parse
from typing import Any, Union

from fastapi.datastructures import QueryParams

from AppMain.settings import AppSettings


def get_frontend_url(path: str) -> str:
    """Return the path of an url in the frontend interface"""
    return urllib.parse.urljoin(AppSettings.FRONTEND_URL, path)


def extract_filter_params(params: Union[dict[str, Any], QueryParams]) -> dict[str, Any]:
    """Extract filters from queryParams.

    example:
        d = {"filter[agency]": "12345"}

        print(extract_filter_params(d))
        > {"agency": "12345"}
    """
    res: dict[str, Any] = {}
    for k, v in params.items():
        k_ = k.replace("filter[", "").replace("]", "")
        res[k_] = v
    return res
