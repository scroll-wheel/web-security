from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup

import requests


def print_success(string, end="\n"):
    print(f"\r\033[1;92m▌\033[00m {string}", end=end)


def print_warning(string, end="\n"):
    print(f"\r\033[1;93m▌\033[00m {string}", end=end)


def print_info(string, end="\n"):
    print(f"\r\033[1;94m▌\033[00m {string}", end=end)


def print_info_secondary(string, end="\n"):
    print(f"\r▌ {string}", end=end)


def print_fail(string):
    print(f"\r\033[1;91m▌\033[00m {string}")
    exit(1)


def print_input(string):
    return input(f"\r\033[1;93m[i]\033[00m {string}")


def auth_lab_usernames():
    resp = requests.get(
        "https://portswigger.net/web-security/authentication/auth-lab-usernames"
    )
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.select_one("code")
    result = query.text.split("\n")
    logger.info("Loaded Authentication lab usernames into memory")
    return result


def auth_lab_passwords():
    resp = requests.get(
        "https://portswigger.net/web-security/authentication/auth-lab-passwords"
    )
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.select_one("code")
    result = query.text.split("\n")
    logger.info("Loaded Authentication lab passwords into memory")
    return result
