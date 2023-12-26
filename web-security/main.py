from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

import importlib
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

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.text

    print_info(f"Using lab title ({title}) to determine module path...")
    resp = requests.get("https://portswigger.net/web-security/all-labs")
    soup = BeautifulSoup(resp.text, "html.parser")

    matchfunc = lambda tag: tag.text == title
    res = soup.find(matchfunc)
    path = res.attrs["href"]
    path = path.split("/")[1:]
    print_info(
        f'Attempting to import function "solve_lab" from module "{".".join(path)}"...'
    )

    package = path[0]
    module = ".".join(path[1:])
    module = importlib.import_module(f".{module}", package)

    solve_lab = getattr(module, "solve_lab")
    print_success("Success. Now attempting to solve lab...\n")
    solve_lab(url, None)

    # TODO: import_module + getattr


def verify_lab_solved(url):
    print_info("Revisiting URL to verify if attack was successful...")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    if soup.select_one("#notification-labsolved"):
        print_success("Attack successful. Lab solved.")
    else:
        print_fail("Lab unsolved. Ensure...")


def main():
    args = get_args()
    root_url = urljoin(args.url, "/")

    verify_lab_accessible(root_url)

    proxies = None
    if args.use_proxy:
        proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}
        print_info('Using "http://127.0.0.1:8080" as a proxy')

    # solve_lab(root_url, proxies)
    verify_lab_solved(root_url)


if __name__ == "__main__":
    main()
