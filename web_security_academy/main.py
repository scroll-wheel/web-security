from web_security_academy.core.lab_session import LabSession
from web_security_academy.core.logger import logger

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from logging import DEBUG, TRACE

import importlib
import argparse
import requests
import urllib3


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-f", "--force-solve", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-x", "--use-proxy", action="store_true")
    return parser.parse_args()


def verify_lab_url(url, args):
    # TODO: Check if given URL is valid

    logger.trace("Checking if given URL is accessible...")
    resp = requests.get(url)
    if resp.status_code == 504:
        logger.failure("URL is inaccessible. Please reopen the lab and use new URL")
        exit(1)

    soup = BeautifulSoup(resp.text, "lxml")
    title = soup.title.text
    logger.info(f"Lab title: {title}")
    if soup.select_one("#notification-labsolved"):
        if args.force_solve:
            logger.warning(
                "Lab already solved. Attempting to resolve may result in a false positive"
            )
        else:
            logger.warning("Lab already solved.")
            exit(1)

    logger.trace("Using lab title to determine module path...")
    resp = requests.get("https://portswigger.net/web-security/all-labs")

    # Return the path of the lab with matching title
    soup = BeautifulSoup(resp.text, "lxml")
    matchfunc = lambda tag: tag.text.strip() == title
    res = soup.find(matchfunc)
    return res.attrs["href"]


def get_solve_lab_func(path):
    module_path = path.replace("/", ".")
    logger.debug(f"Module path: {module_path}")
    try:
        module = importlib.import_module(f"web_security_academy{module_path}.solution")
    except ModuleNotFoundError:
        module = importlib.import_module(f"web_security_academy{module_path}")

    module_solve_lab = getattr(module, "solve_lab")
    logger.debug('Imported "solve_lab" function from module.')
    return module_solve_lab


def verify_lab_solved(url):
    logger.trace("Revisiting URL to verify if attack was successful...")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    if soup.select_one("#notification-labsolved"):
        logger.success("Lab solved.")
    else:
        logger.failure("Lab not solved.")
        exit(1)


def main():
    args = get_args()
    root_url = urljoin(args.url, "/")

    if args.verbose > 1:
        logger.setLevel(TRACE)
        logger.trace("Set logger level to TRACE")
    elif args.verbose == 1:
        logger.setLevel(DEBUG)
        logger.debug("Set logger level to DEBUG")

    path = verify_lab_url(root_url, args)
    solve_lab = get_solve_lab_func(path)

    with LabSession(root_url) as session:
        if args.use_proxy:
            session.proxies = {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080",
            }
            session.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.debug('Using "http://127.0.0.1:8080" as a proxy')
        solve_lab(session)

    verify_lab_solved(root_url)


if __name__ == "__main__":
    main()
