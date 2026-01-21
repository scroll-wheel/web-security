import argparse
import importlib
import re
from urllib.parse import urljoin, urlparse

import httpx
import requests

from web_security_academy.core.lab_session import LabSession
from web_security_academy.core.logger import logger
from web_security_academy.core.utils import bs4

from logging import DEBUG, TRACE  # isort: skip

http_client = None


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-f", "--force-solve", action="store_true")
    parser.add_argument("-r", "--use-requests", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-x", "--use-proxy", action="store_true")
    return parser.parse_args()


def verify_lab_url(url, args):
    hostname = urlparse(url).hostname
    if hostname is None or not re.match(
        r"[0-9a-f]{32}\.web-security-academy\.net",
        hostname,
    ):
        logger.failure("Invalid URL")
        exit(1)

    global http_client
    if args.use_requests:
        logger.trace("Using `requests` library as HTTP client")
        http_client = requests
    else:
        logger.trace("Using `httpx` library as HTTP client")
        http_client = httpx

    logger.trace("Checking if given URL is accessible...")
    resp = http_client.get(url)
    if resp.status_code == 504:
        logger.failure("URL is inaccessible. Please reopen the lab and use new URL")
        exit(1)

    soup = bs4(resp.text)
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
    resp = http_client.get("https://portswigger.net/web-security/all-labs")

    # Return the path of the lab with matching title
    soup = bs4(resp.text)

    def matchfunc(tag):
        return tag.text.strip() == title

    res = soup.find(matchfunc)
    return res.attrs["href"]


def get_solve_lab_func(path):
    module_path = path.replace("/", ".")
    logger.debug(f"Module path: {module_path}")
    try:
        module = importlib.import_module(
            f"web_security_academy{module_path}.{module_path}"
        )
    except ModuleNotFoundError:
        module = importlib.import_module(f"web_security_academy{module_path}")

    module_solve_lab = getattr(module, "solve_lab")
    logger.debug('Imported "solve_lab" function from module.')
    return module_solve_lab


def verify_lab_solved(url):
    logger.trace("Revisiting URL to verify if attack was successful...")
    resp = http_client.get(url)
    soup = bs4(resp.text)
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
        logger.info("Set logger level to TRACE")
    elif args.verbose == 1:
        logger.setLevel(DEBUG)
        logger.info("Set logger level to DEBUG")

    path = verify_lab_url(root_url, args)
    solve_lab = get_solve_lab_func(path)

    session = LabSession(
        root_url,
        use_httpx=not args.use_requests,
        use_proxy=args.use_proxy,
    )
    solve_lab(session)

    verify_lab_solved(root_url)


if __name__ == "__main__":
    main()
