from bs4 import BeautifulSoup

import requests


def print_success(string, end="\n"):
    print(f"\r\033[1;92m[+]\033[00m {string}", end=end)


def print_warning(string, end="\n"):
    print(f"\r\033[1;93m[!]\033[00m {string}", end=end)


def print_info(string, end="\n"):
    print(f"\r\033[1;94m[*]\033[00m {string}", end=end)


def print_info_secondary(string, end="\n"):
    print(f"\r\033[0;36m[?]\033[00m {string}", end=end)


def print_fail(string):
    print(f"\r\033[1;91m[-]\033[00m {string}")
    exit(1)


def print_input(string):
    return input(f"\r\033[1;93m[i]\033[00m {string}")


def get_csrf_token(url, proxies):
    print_info(f'Grabbing CSRF value from "{url}"...')

    s = requests.Session()
    resp = s.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    if csrf is None:
        print_fail("Unable to grab CSRF value.")
    else:
        print_success(f"CSRF value: {csrf}\n")

    return s, csrf
