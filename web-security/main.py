from .utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .lab_session import LabSession

import importlib
import argparse
import requests
import urllib3


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-x", "--use-proxy", action="store_true")
    return parser.parse_args()


def verify_lab_url(url):
    # TODO: Check if given URL is valid

    print_info("Checking if given URL is accessible...")
    resp = requests.get(url)
    if resp.status_code == 504:
        print_fail("URL is inaccessible. Pleace reopen the lab and use new URL.")
    else:
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.text
        print_info_secondary(f"Lab title: {title}")
        print_success(f"URL is accessible.\n")

    print_info(f"Using lab title to determine module path...")
    resp = requests.get("https://portswigger.net/web-security/all-labs")

    # Return the path of the lab with matching title
    soup = BeautifulSoup(resp.text, "html.parser")
    matchfunc = lambda tag: tag.text.strip() == title
    res = soup.find(matchfunc)
    return res.attrs["href"]


def get_solve_lab_func(path):
    path = path.split("/")[1:]
    print_info_secondary(f'Module path: {".".join(path)}')

    package = path[0]
    module = ".".join(path[1:])
    module = importlib.import_module(f".{module}", package)

    module_solve_lab = getattr(module, "solve_lab")
    print_success('Successfully imported "solve_lab" function from module.\n')
    return module_solve_lab


def verify_lab_solved(url):
    print_info("Revisiting URL to verify if attack was successful...")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    if soup.select_one("#notification-labsolved"):
        print_success("Attack successful. Lab solved.")
    else:
        print_fail("Lab not solved.")


def main():
    args = get_args()
    root_url = urljoin(args.url, "/")

    path = verify_lab_url(root_url)
    solve_lab = get_solve_lab_func(path)

    with LabSession(root_url) as session:
        if args.use_proxy:
            session.proxies = {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080",
            }
            session.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            print_info('Using "http://127.0.0.1:8080" as a proxy')
        solve_lab(session, root_url)

    verify_lab_solved(root_url)


if __name__ == "__main__":
    main()
